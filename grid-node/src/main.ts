import GridWorker from './worker.ts?worker';

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <h1>MUKUNDAN 1: Beaver-Grid Test Node</h1>
    <p>Open your browser's Developer Console (F12) to monitor the cryptographic pipeline.</p>
  </div>
`;

console.log("[SYSTEM] Booting Grid Node WebWorker (ESNext Target)...");

// Initialize natively using the Vite import
const worker = new GridWorker();

worker.onerror = (err: ErrorEvent) => {
    console.error("[FATAL WORKER LOAD ERROR]:", err.message || err);
    err.preventDefault(); 
};

worker.onmessage = (e: MessageEvent) => {
    // 1. Catch the new ready ping
    if (e.data.type === 'WORKER_SCRIPT_READY') {
        console.log("[SYSTEM] Worker ES/Wasm modules loaded. Transmitting seed...");
        worker.postMessage({ 
            type: 'INIT_GRID_NODE', 
            payload: { seed: "1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA" } 
        });
    }
    
    // 2. Catch the initialization completion
    if (e.data.type === 'NODE_READY') {
        console.log("[SYSTEM] Node Ready. Commencing ZK-Proof sequence in 2 seconds...");
        setTimeout(() => {
            worker.postMessage({ type: 'COMMENCE_FOLDING' });
        }, 2000);
    }

    // 3. Log ongoing proofs
    if (e.data.type === 'PROOF_CHECKPOINT' || e.data.type === 'MACHINE_HALTED') {
        console.log("[GRID NODE MESSAGE]:", e.data);
    }
};