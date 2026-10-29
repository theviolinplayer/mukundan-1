use wasm_bindgen::prelude::*;
use crate::machine::Machine;
use crate::macro_engine::MacroEngine;

#[derive(Serialize)]
pub struct ExecutionWitness {
    pub step_count: u64,
    pub states: Vec<u8>,
    pub tape_reads: Vec<u8>,
    pub tape_writes: Vec<u8>,
    pub head_movements: Vec<u8>,
}

#[wasm_bindgen]
pub fn execute_and_trace(seed: &str, max_steps: u64) -> JsValue {
    let machine = Machine::from_tnf(seed).expect("Invalid TNF Seed");
    let mut engine = MacroEngine::new();
    let mut witness = ExecutionWitness::new();

    for _ in 0..max_steps {
        if engine.halted { break; }
        witness.record(&engine); 
        engine.step(&machine);
    }
    
    serde_wasm_bindgen::to_value(&witness).unwrap()
}