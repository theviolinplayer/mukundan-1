import init, { WasmNode, P2PNetwork } from '../wasm-bridge/pkg/wasm_bridge.js';
import { Noir } from '@noir-lang/noir_js';
import { BarretenbergBackend } from '@noir-lang/backend_barretenberg';

const ORCHESTRATOR_URL = "http://localhost:3030";
const WS_URL = "ws://localhost:3030/ws";

function bytesToHexLE(bytes) {
    let hex = '0x';
    for (let i = bytes.length - 1; i >= 0; i--) {
        hex += bytes[i].toString(16).padStart(2, '0');
    }
    return hex;
}

async function bootNode() {
    try {
        const wasm = await init();
        postMessage({ type: 'SYS', msg: "Wasm bindings active. Memory safely allocated." });

        let network = new P2PNetwork();
        try {
            await network.connect_signaling_server(WS_URL);
            postMessage({ type: 'SYS', msg: "WebRTC Gossip Protocol active over WebSocket Relay." });
        } catch (e) {
            postMessage({ type: 'ERR', msg: "Signaling server offline." });
        }

        const circuitRes = await fetch('/bb6.json');

        if (!circuitRes.ok) throw new Error(`Artifact fetch failed: HTTP ${circuitRes.status}.`);

        const circuit = await circuitRes.json();
        const backend = new BarretenbergBackend(circuit);
        const noir = new Noir(circuit, backend);

        postMessage({ type: 'SYS', msg: "Noir Barretenberg backend initialized over WebGPU." });

        while (true) {
            try {
                const res = await fetch(`${ORCHESTRATOR_URL}/api/v1/work`);
                const data = await res.json();

                if (data.status === "exhausted" || !data.machine) {
                    postMessage({ type: 'SYS', msg: "Network exhausted." });
                    return;
                }

                postMessage({ type: 'LOG', msg: `[ALLOCATED] Holdout ID: ${data.machine.id}` });

                let node = new WasmNode(data.machine.seed);

                // Fetch the transition logic for the very first step of this chunk
                // to seed the Noir SNARK validator
                const trans = node.get_circuit_transition();

                const startTime = performance.now();
                const chunkSize = 1;

                const ptrBefore = node.get_state_buffer();
                const bufferBefore = new Uint8Array(wasm.memory.buffer, ptrBefore, 112);
                const left_hash_before_str = bytesToHexLE(bufferBefore.slice(0, 32));
                const right_hash_before_str = bytesToHexLE(bufferBefore.slice(32, 64));
                const stepsArrayBefore = new BigUint64Array(wasm.memory.buffer, ptrBefore + 64, 4);
                const steps_before = stepsArrayBefore[0].toString();

                const ptr = node.run_chunk(chunkSize);
                const elapsed = performance.now() - startTime;

                postMessage({ type: 'METRIC', msg: `Computed ${chunkSize} steps in ${elapsed.toFixed(2)}ms.` });
                postMessage({ type: 'SYS', msg: "Solving Execution Witness..." });

                const bufferAfter = new Uint8Array(wasm.memory.buffer, ptr, 112);
                const left_hash_after_str = bytesToHexLE(bufferAfter.slice(0, 32));
                const right_hash_after_str = bytesToHexLE(bufferAfter.slice(32, 64));
                const stepsArrayAfter = new BigUint64Array(wasm.memory.buffer, ptr + 64, 4);
                const steps_after = stepsArrayAfter[0].toString();
                const state_id = new Uint32Array(wasm.memory.buffer, ptr + 96, 1)[0];
                const status = new Uint32Array(wasm.memory.buffer, ptr + 100, 1)[0];

                const rootBytes = node.get_tnf_root();
                const rootField = bytesToHexLE(rootBytes);

                const pathBytes = node.get_tnf_path(trans[0], trans[1]);
                const pathFields = [];
                for (let i = 0; i < 4; i++) {
                    pathFields.push(bytesToHexLE(pathBytes.slice(i * 32, (i + 1) * 32)));
                }

                const circuitInputs = {
                    current_state: { state: trans[0].toString(), head_symbol: trans[1].toString(), left_tape_hash: left_hash_before_str, right_tape_hash: right_hash_before_str, steps_accumulated: steps_before },
                    next_state: { state: trans[4].toString(), head_symbol: "0", left_tape_hash: left_hash_after_str, right_tape_hash: right_hash_after_str, steps_accumulated: steps_after },
                    transition_write: trans[2].toString(),
                    transition_next_move: trans[3].toString(),
                    transition_next_state: trans[4].toString(),
                    tnf_merkle_root: rootField,
                    tnf_merkle_path: pathFields,
                    compressed_block_count: "1",
                    prev_left_tape_preimage: [trans[1].toString(), "1"],
                    prev_right_tape_preimage: [trans[1].toString(), "1"]
                };

                let proofHex = "";
                try {
                    const { witness } = await noir.execute(circuitInputs);
                    postMessage({ type: 'SYS', msg: "Witness solved! Compiling ZK-SNARK Proof via WebGPU..." });
                    const proofData = await backend.generateProof(witness);
                    proofHex = Array.from(proofData.proof).map(b => b.toString(16).padStart(2, '0')).join('');
                } catch (noirError) {
                    postMessage({ type: 'ERR', msg: `Strict constraint check failed: ${noirError.message}` });
                    throw noirError;
                }

                postMessage({ type: 'METRIC', msg: `[SUCCESS] Proof Generated. SNARK Size: ${proofHex.length / 2} bytes.` });

                const response = await fetch(`${ORCHESTRATOR_URL}/api/v1/submit`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        machine_id: data.machine.id,
                        checkpoint: {
                            total_steps: steps_after,
                            state: state_id,
                            head_symbol: trans[1],
                            left_tape_hash: Array.from(bufferAfter.slice(0, 32)),
                            right_tape_hash: Array.from(bufferAfter.slice(32, 64))
                        },
                        proof: proofHex
                    })
                });

                const result = await response.json();
                if (result.status !== "success") {
                    throw new Error(`Server Rejected Proof: ${result.message}`);
                }
                postMessage({ type: 'SYS', msg: `[NETWORK GATE] CHECKPOINT & PROOF ACCEPTED.` });
                node.free();

                // Allow the worker to naturally loop back and pull the next chunk

            } catch (error) {
                postMessage({ type: 'ERR', msg: `Node Failure: ${error.message}` });
                await new Promise(r => setTimeout(r, 5000));
            }
        }
    } catch (fatalError) {
        postMessage({ type: 'ERR', msg: `CRITICAL BOOT FAILURE: ${fatalError.message}` });
    }
}

bootNode();