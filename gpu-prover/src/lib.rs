use wgpu::util::DeviceExt;
use bytemuck::{Pod, Zeroable};

// MUKUNDAN 1 - Memory-Aligned Cryptographic Structs
// These strictly mirror the WGSL definitions to prevent VRAM alignment faults.

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable, Debug, Default)]
pub struct U256 {
    pub limbs: [u32; 8],
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable, Debug, Default)]
pub struct PointAffine {
    pub x: U256,
    pub y: U256,
}

/// Dispatches the Multi-Scalar Multiplication to the client's GPU.
pub async fn execute_msm_kernel(scalars: &[U256], bases: &[PointAffine]) -> Vec<PointAffine> {
    assert_eq!(scalars.len(), bases.len(), "MSM Arity Mismatch: Scalars and Bases must be equal length.");
    let instance_count = scalars.len();

    // 1. Initialize WebGPU Context
    let instance = wgpu::Instance::default();
    let adapter = instance
        .request_adapter(&wgpu::RequestAdapterOptions::default())
        .await
        .expect("Fatal: WebGPU not supported on this client browser.");
        
    let (device, queue) = adapter
        .request_device(&wgpu::DeviceDescriptor::default(), None)
        .await
        .expect("Fatal: Failed to acquire logical GPU device.");

    // 2. Load the WGSL Kernel
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("BN254 MSM Kernel"),
        source: wgpu::ShaderSource::Wgsl(include_str!("bn254_msm.wgsl").into()),
    });

    // 3. Allocate VRAM Buffers
    let scalars_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("Scalars VRAM Buffer"),
        contents: bytemuck::cast_slice(scalars),
        usage: wgpu::BufferUsages::STORAGE,
    });

    let bases_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("Bases VRAM Buffer"),
        contents: bytemuck::cast_slice(bases),
        usage: wgpu::BufferUsages::STORAGE,
    });

    let results_buffer_size = (instance_count * std::mem::size_of::<PointAffine>()) as wgpu::BufferAddress;
    let results_buffer = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("Results VRAM Buffer"),
        size: results_buffer_size,
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
        mapped_at_creation: false,
    });

    // We need a staging buffer to pull data from VRAM back to the Wasm CPU thread
    let staging_buffer = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("Results Staging Buffer"),
        size: results_buffer_size,
        usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });

    // 4. Construct the Compute Pipeline & Bind Groups
    let compute_pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("MSM Compute Pipeline"),
        layout: None,
        module: &shader,
        entry_point: "main",
    });

    let bind_group_layout = compute_pipeline.get_bind_group_layout(0);
    let bind_group = device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("MSM Bind Group"),
        layout: &bind_group_layout,
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: scalars_buffer.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: bases_buffer.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 2,
                resource: results_buffer.as_entire_binding(),
            },
        ],
    });

    // 5. Encode GPU Commands and Dispatch
    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor { label: None });
    {
        let mut cpass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor { label: None, timestamp_writes: None });
        cpass.set_pipeline(&compute_pipeline);
        cpass.set_bind_group(0, &bind_group, &[]);
        // Calculate workgroups based on @workgroup_size(64) in WGSL
        let workgroup_count = ((instance_count as u32) + 63) / 64; 
        cpass.dispatch_workgroups(workgroup_count, 1, 1);
    }

    // Copy results from GPU Storage to the Staging Buffer
    encoder.copy_buffer_to_buffer(&results_buffer, 0, &staging_buffer, 0, results_buffer_size);
    queue.submit(Some(encoder.finish()));

    // 6. Map Memory and Await Readback
    let buffer_slice = staging_buffer.slice(..);
    let (sender, receiver) = futures_intrusive::channel::shared::oneshot_channel();
    buffer_slice.map_async(wgpu::MapMode::Read, move |v| sender.send(v).unwrap());

    // In a browser environment, device.poll() is handled automatically, 
    // but we enforce it here for universal compatibility.
    device.poll(wgpu::Maintain::Wait);
    receiver.receive().await.unwrap().unwrap();

    // 7. Extract the Cryptographic Data
    let data = buffer_slice.get_mapped_range();
    let result: Vec<PointAffine> = bytemuck::cast_slice(&data).to_vec();
    
    drop(data);
    staging_buffer.unmap();

    result
}