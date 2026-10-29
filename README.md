# MUKUNDAN 1
### Verifiable Distributed Computation Engine for the Busy Beaver BB(6) Challenge

[![Rust](https://img.shields.io/badge/rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![Noir](https://img.shields.io/badge/noir-0.36.0-black.svg)](https://noir-lang.org/)
[![WebGPU](https://img.shields.io/badge/webgpu-WGSL-blue.svg)](https://www.w3.org/TR/webgpu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MUKUNDAN 1 is a decentralized, zero-knowledge verifiable compute infrastructure designed to tackle open problems in computability theory—specifically the classification of the **1,161 remaining holdout Turing machines in the Busy Beaver BB(6) challenge**.

Following the collective 2024 resolution of BB(5), the 6-state Busy Beaver problem remains an active frontier. MUKUNDAN 1 transforms untrusted web browsers into verifiable compute nodes using WebAssembly, zero-knowledge SNARKs (Noir), and WebGPU acceleration.

---

## 🏛️ Architecture Overview

```text
+-------------------------------------------------------------+
|                       MUKUNDAN 1                            |
+------------------+------------------+-----------------------+
|                  |                  |                       |
|  +-----------+   |  +-----------+   |  +-----------------+  |
|  | Python    |   |  | Rust      |   |  |  Browser Node   |  |
|  | Pipeline  |---+->| Server    |<-+- -|  (Web Worker)   |  |
|  |           |   |  | (Warp)    |   |  +-----------------+  |
|  +-----------+   |  +-----+-----+   |  | Rust -> WASM    |  |
|  holdouts.json   |        |         |  | MacroEngine     |  |
|                  |   WebSocket      |  |      |          |  |
|                  |   Signaling      |  | Noir ZK-SNARK   |  |
|                  |        |         |  | Prover          |  |
|                  |        v         |  |      |          |  |
|                  |  +-----------+   |  | WebGPU MSM      |  |
|                  |  | WebRTC    |<--+--| (Accelerator)   |  |
|                  |  | P2P Mesh  |   |  +-----------------+  |
|                  |  +-----------+   |                       |
|  +-----------+   |                  |                       |
|  | Noir      |   |                  |                       |
|  | Circuit   |---+------------------+-> ZK Verification     |
|  | (ACIR)    |   |                  |   Poseidon Merkle     |
|  +-----------+   |                  |   Transition Tree     |
+------------------+------------------+-----------------------+
```

---

## 🔬 Core Innovations

### 1. $O(1)$ Poseidon Hash-Chain Tape Stack (`core/src/macro_engine.rs`)
Turing machines have infinite memory, whereas ZK-SNARK circuits require fixed-size constraint systems. Storing or unrolling tape memory inside a circuit causes constraint explosion. 
- MUKUNDAN 1 models the tape as two directional stacks of run-length-encoded symbol blocks.
- Each block is committed into a rolling Poseidon hash chain: $\text{Hash}_{i} = \mathcal{H}(\text{symbol}, \text{count}, \text{Hash}_{i-1})$.
- The ZK circuit only validates local hash transitions (pushes and pops), verifying unbounded tape modifications with **two 32-byte field elements**.

### 2. Transition Table Merkle Commitments (`core/src/tnf_tree.rs`, `circuits/src/main.nr`)
- The 12 state-symbol transition rules of each 6-state machine are committed into a depth-4 Poseidon Merkle tree.
- The root hash commits the immutable machine definition. Every proven step provides a 4-sibling authentication path to prove strict adherence to the machine's rule table.

### 3. Zero-Copy WASM $\leftrightarrow$ JS Memory Layout (`wasm-bridge/src/lib.rs`)
- Uses `#[repr(C, align(16))]` for `CheckpointLayout`.
- `run_chunk()` returns raw pointers into WASM linear memory, enabling the client JavaScript runtime to directly construct TypedArray views (`BigUint64Array`, `Uint8Array`) with zero serialization overhead.

### 4. WebGPU Finite-Field Arithmetic Shader (`gpu-prover/src/bn254_msm.wgsl`)
- Implements U256 multi-precision arithmetic (8x 32-bit limbs with manual carry/borrow propagation) and prime field modular reduction directly in WGSL for the BN254 curve ($q = 21888242871839275222246405745257275088696311157297823662689037894645226208583$).

---

## 📦 Project Structure

```
mukundan-1/
├── circuits/           # Noir ZK-SNARK circuit definitions & constraints
│   ├── src/main.nr     # Transition and step verification circuit
│   └── src/memory.nr   # Memory multiset consistency arguments
├── core/               # Rust simulation engine (compiles to native & wasm32)
│   ├── src/macro_engine.rs # Macro-stepping engine with Poseidon hash-chain
│   ├── src/smt.rs          # Depth-64 Sparse Merkle Tree
│   └── src/tnf_tree.rs     # Transition table Merkle tree
├── wasm-bridge/        # WebAssembly bindings & WebRTC DataChannel networking
├── gpu-prover/         # WebGPU WGSL compute shader for BN254 MSM
├── server/             # Warp orchestrator and holdout scheduler
├── client/             # Web Worker client pipeline with NoirJS & Barretenberg
├── data/               # 1,161 canonical BB(6) holdout definitions
└── scripts/            # Synchronization pipeline from bbchallenge.org
```

---

## 🚀 Getting Started

### Prerequisites
- [Rust](https://rustup.rs/) (v1.75+)
- [Node.js](https://nodejs.org/) (v18+)
- [Nargo](https://noir-lang.org/docs/getting_started/installation/) (v0.36.0)
- [wasm-pack](https://rustwasm.github.io/wasm-pack/installer/)

### 1. Build and Run the Orchestrator
```bash
cargo run --package mukundan-server
```
The server will initialize the grid scheduler and ingest all 1,161 holdout machines from `data/holdouts.json`.

### 2. Start the Volunteer Browser Node
```bash
cd client
npm install
npm run dev
```
Navigate to `http://localhost:5173` and click **Initialize Verifiable Worker** to begin processing assigned machines, solving execution witnesses, and generating ZK proofs.

---

## 🛠️ Status & Transparent Limitations

- **Pippenger Bucket Accumulation:** U256 addition, subtraction, comparison, and modular reduction are fully implemented in `bn254_msm.wgsl`. The Pippenger accumulation loop across base points is currently an architectural stub.
- **Recursive Folding (IVC):** Currently verifies macro-steps individually. Incremental Verifiable Computation (Protogalaxy / Nova) is planned to fold thousands of execution steps into a single recurring proof.
- **Persistence:** Scheduler state is maintained in-memory for active sessions (`server/src/db_connector.rs` persistence is in progress).
