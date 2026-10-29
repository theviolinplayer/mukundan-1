import { BarretenbergBackend } from '@noir-lang/backend_barretenberg';
import { Noir } from '@noir-lang/noir_js';
import circuitJson from '../../circuits/target/mukundan_circuits.json';
import { WasmNode } from './pkg/wasm_bridge.js';

const circuit = circuitJson as any;

let backend: BarretenbergBackend;
let noir: Noir;
let wasmNode: WasmNode;

console.log("[WORKER] Script evaluated. Awaiting INIT command...");
self.postMessage({ type: 'WORKER_SCRIPT_READY' });

self.onmessage = async (e) => {
    try {
        const { type, payload } = e.data;

        if (type === 'INIT_GRID_NODE') {
            console.log("[WORKER] 1/3: Booting Barretenberg Backend...");
            backend = new BarretenbergBackend(circuit);
            
            console.log("[WORKER] 2/3: Initializing Noir...");
            noir = new Noir(circuit); 
            
            console.log("[WORKER] 3/3: Instantiating WasmNode with TNF Seed...");
            wasmNode = new WasmNode(payload.seed);
            
            console.log("[WORKER] ALL SYSTEMS GREEN. Emitting NODE_READY...");
            self.postMessage({ type: 'NODE_READY' });
        }

        if (type === 'COMMENCE_FOLDING') {
            let stepCount = 0;
            let accumulator = null;

            // Helper to strictly format inputs as base-10 strings for Noir Fields
            const field = (val: string | number) => {
                try {
                    let bn = BigInt(val);
                    // Clamp negative states (like -1 halt states) to 0 for Field compatibility
                    return bn < 0n ? "0" : bn.toString(10);
                } catch {
                    return "0";
                }
            };

            while (true) {
                const chunkPayload = wasmNode.run_chunk(1);
                
                const [
                    status, steps, current_state_val, left_hash, right_hash, 
                    p_state, head, write, n_move, n_state
                ] = chunkPayload.split('|');

                stepCount = parseInt(steps);

                if (status === "HALT") {
                    console.log(`[WORKER] Machine halted at step ${stepCount}`);
                    break;
                }

                // Map exactly to main.nr types using pure decimal strings
                const proofInputs = {
                    current_state: {
                        state: field(p_state),
                        head_symbol: field(head), 
                        left_tape_hash: field(left_hash),
                        right_tape_hash: field(right_hash),
                        steps_accumulated: field(stepCount - 1)
                    },
                    next_state: {
                        state: field(n_state), 
                        head_symbol: field(0), 
                        left_tape_hash: field(left_hash),
                        right_tape_hash: field(right_hash),
                        steps_accumulated: field(stepCount)
                    },
                    transition_write: field(write),
                    transition_next_move: field(n_move),
                    transition_next_state: field(n_state),
                    compressed_block_count: field(1),
                    prev_left_tape_preimage: [field(head), field(1)],
                    prev_right_tape_preimage: [field(head), field(1)],
                    tnf_merkle_path: ["0", "0", "0", "0"] 
                };

                const { witness } = await noir.execute(proofInputs);
                const proof = await backend.generateProof(witness);
                
                accumulator = proof;

                self.postMessage({ 
                    type: 'PROOF_CHECKPOINT', 
                    steps: stepCount, 
                    proof: accumulator 
                });
            }

            self.postMessage({ 
                type: 'MACHINE_HALTED', 
                final_proof: accumulator 
            });
        }
    } catch (error) {
        console.error("[CRITICAL WORKER CRASH]:", error);
    }
};