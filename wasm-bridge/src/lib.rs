pub mod network;

use mukundan_core::machine::Machine;
use mukundan_core::macro_engine::MacroEngine;
use mukundan_core::tnf_tree::TnfTree;
use mukundan_core::hash::u8_array_from_fr;
use wasm_bindgen::prelude::*;

const TAPE_DEPTH: usize = 256;

#[repr(C, align(16))]
pub struct CheckpointLayout {
    pub left_hash: [u8; 32],
    pub right_hash: [u8; 32],
    pub steps: [u64; 4],
    pub state_id: u32,
    pub status: u32, // 0 = RUNNING, 1 = HALTED
    _padding: [u64; 1],
}

#[wasm_bindgen]
pub struct WasmNode {
    engine: MacroEngine<TAPE_DEPTH>,
    machine: Machine,
    tnf_tree: TnfTree,
    buffer: CheckpointLayout,
}

#[wasm_bindgen]
impl WasmNode {
    #[wasm_bindgen(constructor)]
    pub fn new(tnf_seed: &str) -> Result<WasmNode, JsValue> {
        let machine = Machine::from_tnf(tnf_seed)
            .map_err(|_| JsValue::from_str("INVALID_TNF_SEED"))?;
        let tnf_tree = TnfTree::new(&machine);
            
        Ok(WasmNode {
            engine: MacroEngine::new(),
            machine,
            tnf_tree,
            buffer: CheckpointLayout {
                left_hash: [0; 32], right_hash: [0; 32],
                steps: [0; 4], state_id: 0, status: 0, _padding: [0; 1],
            }
        })
    }

    #[wasm_bindgen]
    pub fn run_chunk(&mut self, chunk_size: u32) -> *const u8 {
        for _ in 0..chunk_size {
            if self.engine.halted {
                self.buffer.status = 1;
                break;
            }
            self.engine.step(&self.machine);
        }
        
        self.buffer.left_hash = self.engine.tape_left.current_hash();
        self.buffer.right_hash = self.engine.tape_right.current_hash();
        self.buffer.steps = self.engine.total_steps.0;
        self.buffer.state_id = self.engine.state as u32;

        &self.buffer as *const _ as *const u8
    }

    #[wasm_bindgen]
    pub fn get_state_buffer(&mut self) -> *const u8 {
        self.buffer.left_hash = self.engine.tape_left.current_hash();
        self.buffer.right_hash = self.engine.tape_right.current_hash();
        self.buffer.steps = self.engine.total_steps.0;
        self.buffer.state_id = self.engine.state as u32;
        self.buffer.status = if self.engine.halted { 1 } else { 0 };
        &self.buffer as *const _ as *const u8
    }

    #[wasm_bindgen]
    pub fn get_tnf_root(&self) -> js_sys::Uint8Array {
        let root_fr = self.tnf_tree.root();
        let arr = u8_array_from_fr(root_fr);
        js_sys::Uint8Array::from(&arr[..])
    }
    
    #[wasm_bindgen]
    pub fn get_tnf_path(&self, state: usize, symbol: usize) -> js_sys::Uint8Array {
        let path_fr = self.tnf_tree.get_path(state, symbol);
        let mut result = [0u8; 128];
        for (i, p) in path_fr.iter().enumerate() {
            let arr = u8_array_from_fr(*p);
            result[i*32..(i+1)*32].copy_from_slice(&arr);
        }
        js_sys::Uint8Array::from(&result[..])
    }

    #[wasm_bindgen]
    pub fn get_circuit_transition(&self) -> js_sys::Uint32Array {
        let (state_in, read_sym, _) = self.engine.get_state_commitment();
        let state_in_idx = if state_in < 0 { 0 } else { state_in as usize };
        let sym_idx = read_sym as usize;
        let t = self.machine.transitions[state_in_idx][sym_idx];
        
        let mut result = [0u32; 5];
        result[0] = state_in_idx as u32;
        result[1] = sym_idx as u32;
        if let Some(trans) = t {
            result[2] = trans.write as u32;
            result[3] = match trans.next_move {
                mukundan_core::machine::Move::Left => 0,
                mukundan_core::machine::Move::Right => 1,
            };
            result[4] = if trans.next_state < 0 { 0 } else { trans.next_state as u32 };
        }
        
        js_sys::Uint32Array::from(&result[..])
    }
}