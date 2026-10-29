import init, { WasmNode } from './pkg/wasm_bridge.js';

async function runGridNode() {
    await init();
    console.log("--- Beaver-Grid Wasm Execution Layer Online ---");

    while (true) {
        try {
            // 1. Request a pending BB(6) machine from the Orchestrator
            const res = await fetch("http://127.0.0.1:3030/api/v1/work");
            const data = await res.json();
            
            if (data.status === "exhausted" || !data.machine) {
                console.log("Grid pool exhausted. Polling in 5s...");
                await new Promise(r => setTimeout(r, 5000));
                continue;
            }

            const holdout = data.machine;
            console.log(`Computing Checkpoint for Seed: ${holdout.seed}`);

            // 2. Initialize Sandboxed Wasm Engine
            const node = new WasmNode(holdout.seed);
            
            // 3. Execute 10,000 steps per frame to prevent thread lock
            const payload = node.run_chunk(10000);
            const [status, steps, state, left_hash, right_hash] = payload.split('|');

            // 4. Submit State & Cryptographic Proof
            await fetch("http://127.0.0.1:3030/api/v1/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    machine_id: holdout.id,
                    checkpoint: {
                        total_steps: steps,
                        state: parseInt(state),
                        head_symbol: 0, 
                        left_tape_hash: Array(32).fill(0), // Placeholder for Poseidon root
                        right_tape_hash: Array(32).fill(0)
                    },
                    proof: "0xDUMMY_SNARK_PROOF_FOR_NETWORK_TESTING" 
                })
            });

            if (status === "HALT") {
                console.log(`Machine ${holdout.id} Halted at step ${steps}.`);
            }
        } catch (err) {
            console.error("Node disconnected from Orchestrator. Retrying...", err);
            await new Promise(r => setTimeout(r, 5000));
        }
    }
}

runGridNode();