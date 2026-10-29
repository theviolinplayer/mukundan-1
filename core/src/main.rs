// core/src/main.rs
pub mod machine;
pub mod macro_engine;

use machine::Machine;
use macro_engine::MacroEngine;

fn main() {
    println!("--- MUKUNDAN 1: BB(6) Execution Node ---");
    
    // Default testing seed (BB(6) Holdout)
    let seed = "1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA";
    let machine = Machine::from_tnf(seed).expect("CRITICAL: Failed to parse TNF seed.");
    let mut engine = MacroEngine::<2048>::new();

    println!("Targeting Machine TNF: {}", seed);
    println!("Executing macro-machine sequence...");

    // Execute a standard block of transitions
    for _ in 0..10_000 {
        engine.step(&machine);
        if engine.halted {
            break;
        }
    }

    println!("Execution Checkpoint Reached.");
    println!("Actual Turing Steps Simulated: {}", engine.total_steps);
    println!("Machine Halted: {}", engine.halted);
    println!("Current State (0=A, 5=F): {}", engine.state);
    
    // Future integration point for ZK-Witness Generation
    // generate_noir_witness(&engine); 
}