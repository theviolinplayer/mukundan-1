// server/src/scheduler.rs
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::fs;

// The Cryptographic Checkpoint representing a frozen Wasm state
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct StateCheckpoint {
    pub total_steps: String, // Stored as string to natively handle BigUint serialization
    pub state: u8,
    pub head_symbol: u8,
    pub left_tape_hash: [u8; 32],  // Future IVC Poseidon root
    pub right_tape_hash: [u8; 32], // Future IVC Poseidon root
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct HoldoutMachine {
    pub id: String,
    pub seed: String,
    pub current_checkpoint: Option<StateCheckpoint>,
    pub status: MachineStatus,
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
pub enum MachineStatus {
    Pending,
    Computing,
    Halted,
    ProvenInfinite, // Required for Lin Recurrence detection
}

pub struct GridScheduler {
    // Thread-safe state tree of all 1,161 holdouts
    machines: Arc<Mutex<HashMap<String, HoldoutMachine>>>,
}

impl GridScheduler {
    pub fn new() -> Self {
        Self {
            machines: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    /// Ingests the baseline JSON holdouts into the active memory pool
    pub fn load_baseline(&self, filepath: &str) {
        let data = fs::read_to_string(filepath).expect("CRITICAL: Failed to read holdouts.json");
        let json: serde_json::Value = serde_json::from_str(&data).expect("Invalid JSON payload");
        
        let mut map = self.machines.lock().unwrap();
        if let Some(holdouts) = json.get("holdouts").and_then(|h| h.as_array()) {
            for h in holdouts {
                let id = h["id"].as_str().unwrap().to_string();
                let seed = h["seed"].as_str().unwrap().to_string();
                map.insert(id.clone(), HoldoutMachine {
                    id,
                    seed,
                    current_checkpoint: None,
                    status: MachineStatus::Pending,
                });
            }
        }
        println!("Beaver-Grid Scheduler Initialized: {} Holdouts ingested.", map.len());
    }

    /// Dispatches a chunk of work to a requesting WebWorker node
    pub fn request_work_chunk(&self) -> Option<HoldoutMachine> {
        let mut map = self.machines.lock().unwrap();
        
        // Priority Routing: Find the first pending machine
        for (_, machine) in map.iter_mut() {
            if machine.status == MachineStatus::Pending {
                machine.status = MachineStatus::Computing;
                return Some(machine.clone());
            }
        }
        None
    }

    /// Ingests an updated checkpoint from a browser node returning work
    pub fn submit_checkpoint(&self, machine_id: &str, checkpoint: StateCheckpoint) -> Result<(), &'static str> {
        let mut map = self.machines.lock().unwrap();
        if let Some(machine) = map.get_mut(machine_id) {
            
            // ARCHITECTURAL GATING: 
            // In the final protocol, the server MUST verify the ZK-SNARK proof 
            // before replacing the canonical state checkpoint.
            
            machine.current_checkpoint = Some(checkpoint);
            machine.status = MachineStatus::Pending; // Release back to pool for the next N-step chunk
            
            Ok(())
        } else {
            Err("Machine ID not found in canonical state tree.")
        }
    }
}