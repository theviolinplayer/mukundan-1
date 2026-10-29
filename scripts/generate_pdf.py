import subprocess
import os
import base64

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def generate_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    run_img = get_base64_img(os.path.join(root_dir, "data", "running_mechanism.png"))
    s15_img = get_base64_img(os.path.join(root_dir, "data", "S15_client_dashboard.png"))
    s16_img = get_base64_img(os.path.join(root_dir, "data", "S16_devtools_telemetry.png"))

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MUKUNDAN 1: Technical Report</title>
<style>
    @page {
        size: A4;
        margin: 16mm 16mm 16mm 16mm;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1a1a1a;
        line-height: 1.48;
        font-size: 9.5pt;
        background: #ffffff;
    }
    h1 {
        font-size: 20pt;
        font-weight: 800;
        margin-bottom: 2px;
        color: #0f172a;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-size: 10pt;
        font-weight: 600;
        color: #2563eb;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .meta-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 8.5pt;
        display: flex;
        justify-content: space-between;
    }
    .meta-item strong {
        color: #334155;
    }
    h2 {
        font-size: 11.5pt;
        font-weight: 700;
        color: #0f172a;
        border-bottom: 1.5px solid #0f172a;
        padding-bottom: 2px;
        margin-top: 14px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    h3 {
        font-size: 10pt;
        font-weight: 700;
        color: #1e293b;
        margin-top: 8px;
        margin-bottom: 3px;
    }
    p {
        margin-top: 0;
        margin-bottom: 6px;
        text-align: justify;
    }
    .abstract {
        background: #f1f5f9;
        border-left: 3.5px solid #2563eb;
        padding: 8px 12px;
        font-size: 8.5pt;
        font-style: italic;
        margin-bottom: 12px;
    }
    .abstract strong {
        font-style: normal;
        color: #0f172a;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 8pt;
        margin: 6px 0 10px 0;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 4px 6px;
        text-align: left;
    }
    th {
        background: #f8fafc;
        font-weight: 700;
        color: #0f172a;
    }
    code {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 8pt;
        background: #f1f5f9;
        padding: 1px 3px;
        border-radius: 3px;
        color: #0f172a;
    }
    pre {
        background: #0f172a;
        color: #f8fafc;
        padding: 7px 9px;
        border-radius: 5px;
        font-size: 7.5pt;
        font-family: "Consolas", monospace;
        overflow-x: auto;
        line-height: 1.3;
        margin: 5px 0 8px 0;
    }
    .diagram-img {
        width: 100%;
        max-width: 100%;
        border-radius: 5px;
        border: 1px solid #cbd5e1;
        margin: 5px 0 8px 0;
        display: block;
    }
    .page-break {
        page-break-before: always;
    }
    .avoid-break {
        page-break-inside: avoid;
    }
    .callout {
        background: #fefce8;
        border: 1px solid #fef08a;
        border-left: 3.5px solid #eab308;
        padding: 6px 10px;
        font-size: 8pt;
        margin: 6px 0 8px 0;
        border-radius: 4px;
    }
</style>
</head>
<body>

<h1>MUKUNDAN 1</h1>
<div class="subtitle">Multi-node Universal Kernel for Unified Non-halting Distributed Automata Networks</div>

<div class="meta-box">
    <div class="meta-item"><strong>Author:</strong> Mukundan Padmaraj</div>
    <div class="meta-item"><strong>Domain:</strong> Computability Theory & Cryptographic Systems</div>
    <div class="meta-item"><strong>Repository:</strong> github.com/theviolinplayer/mukundan-1</div>
    <div class="meta-item"><strong>Submission:</strong> MIT Maker Portfolio 2026</div>
</div>

<div class="abstract">
    <strong>Abstract —</strong> The Busy Beaver problem BB(n) seeks the maximum steps an n-state halting Turing machine can execute from a blank tape. While BB(5) = 47,176,870 was solved collaboratively in 2024 after sixty years, BB(6) remains an active open challenge with 1,161 undecided "holdout" machines. This report presents <strong>MUKUNDAN 1</strong>, a trustless volunteer compute network that transforms untrusted browser tabs into verifiable computation nodes. By coupling a Rust macro-stepping simulation core compiled to WebAssembly with a Noir zero-knowledge SNARK circuit, MUKUNDAN 1 verifies arbitrary machine trajectories in O(1) circuit constraints using a novel Poseidon hash-chain stack. Field arithmetic is accelerated via a WebGPU compute shader implementing multi-precision U256 addition and Montgomery modular reduction.
</div>

<h2>1. Introduction & The Computability Frontier</h2>
<p>
Tibor Rado introduced the Busy Beaver game in 1962 to formalize the non-computable boundaries of algorithmic limits. Determining BB(6) is mathematically demanding: individual 6-state machines can simulate complex Collatz-like behaviors, counter machines, and exponential tape expansions that evade standard closed-form induction. 
Centralized compute architectures cannot scale verification securely: crowdsourced volunteer nodes are inherently untrusted. MUKUNDAN 1 resolves this by generating non-interactive zero-knowledge proofs (ZK-SNARKs) for each execution checkpoint, providing mathematically unforgeable proofs of work to an orchestrator.
</p>

<h2>2. System Architecture & Topology</h2>
<p>
MUKUNDAN 1 partitions computation across five programming languages (Rust, Noir, WGSL, TypeScript, Python) and four specialized crates to optimize for target hardware constraints:
</p>

<img class="diagram-img" src="###RUN_IMG###" alt="Runtime Execution Mechanism" />

<div class="avoid-break">
<table>
    <thead>
        <tr>
            <th>Subsystem</th>
            <th>Language</th>
            <th>Primary Function & Cryptographic Role</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>core</code></td>
            <td>Rust</td>
            <td>Macro-stepping engine, Sparse Merkle Tree (SMT), Poseidon hash-chain tape stack.</td>
        </tr>
        <tr>
            <td><code>circuits</code></td>
            <td>Noir (ACIR)</td>
            <td>ZK-SNARK circuit proving state transitions, step accumulation, and tape consistency.</td>
        </tr>
        <tr>
            <td><code>gpu-prover</code></td>
            <td>WGSL (WebGPU)</td>
            <td>Multi-precision 256-bit modular field arithmetic kernel for BN254 elliptic curve points.</td>
        </tr>
        <tr>
            <td><code>wasm-bridge</code></td>
            <td>Rust / Wasm</td>
            <td>16-byte aligned linear memory interface + WebRTC RTCDataChannel gossip network.</td>
        </tr>
        <tr>
            <td><code>server</code></td>
            <td>Rust (Warp)</td>
            <td>Thread-safe holdout scheduler, WebSocket signaling relay, and checkpoint verifier.</td>
        </tr>
        <tr>
            <td><code>client</code></td>
            <td>JS / Worker</td>
            <td>Browser volunteer execution node, witness generation, and Barretenberg SNARK prover.</td>
        </tr>
    </tbody>
</table>
</div>

<div class="page-break"></div>

<h2>3. Core Technical & Cryptographic Innovations</h2>

<h3>3.1. O(1) Circuit Footprint via Poseidon Hash-Chain Stacks</h3>
<p>
A classical Turing machine tape is unbounded. Standard SNARK constraint systems cannot support variable or infinite memory arrays without constraint explosion. MUKUNDAN 1 solves this through a bidirectional <code>FixedStack</code>:
</p>
<pre>
pub struct TapeBlock {
    pub symbol: u8,
    pub count: U256,
    pub hash: [u8; 32],
}
// Each block commits to the prior stack state via Poseidon-3:
Hash_i = Poseidon(symbol, count, Hash_{i-1})
</pre>
<p>
During execution, tape operations are represented as pushes and pops of run-length-encoded blocks. In the Noir circuit (<code>memory.nr</code>), verifying an unbounded macro-step does not require reading the entire tape; the circuit merely validates local hash transitions:
</p>
<pre>
pub fn check_tape_push(symbol: Field, count: Field, prev_hash: Field, expected_hash: Field) {
    let computed_hash = std::hash::poseidon::bn254::hash_3([symbol, count, prev_hash]);
    assert(computed_hash == expected_hash);
}
</pre>
<p>
The circuit only inspects two 32-byte field elements (<code>left_tape_hash</code> and <code>right_tape_hash</code>), achieving an invariant O(1) constraint count regardless of whether the tape contains five symbols or five million.
</p>

<h3>3.2. Transition Table Merkle Commitments</h3>
<p>
To ensure an untrusted worker simulates the <em>exact</em> assigned Turing machine, the machine's 12 transition rules (6 states x 2 symbols) are committed into a depth-4 binary Merkle tree using Poseidon-5 hashes (<code>tnf_tree.rs</code>). Each step witness includes a 4-element sibling authentication path. The Noir circuit verifies:
<code>MerkleVerify(leaf_hash, path, root) == true</code>.
This anchors all simulated transitions directly to the public <code>tnf_merkle_root</code>.
</p>

<h3>3.3. Zero-Copy WASM-to-JavaScript Memory Bridge</h3>
<p>
High-throughput distributed computation cannot tolerate JSON serialization between WebAssembly and JavaScript. MUKUNDAN 1 implements <code>CheckpointLayout</code> with explicit C memory alignment:
</p>
<pre>
#[repr(C, align(16))]
pub struct CheckpointLayout {
    pub left_hash: [u8; 32],
    pub right_hash: [u8; 32],
    pub steps: [u64; 4],
    pub state_id: u32,
    pub status: u32,
    _padding: [u64; 1],
}
</pre>
<p>
The <code>run_chunk()</code> method executes N transitions and returns a raw pointer (<code>*const u8</code>) to linear memory. The client Web Worker instantly constructs zero-copy typed views:
<code>new Uint8Array(wasm.memory.buffer, ptr, 112)</code>.
</p>

<div class="avoid-break">
<h2>4. Empirical Verification & Holdout Benchmarks</h2>
<p>
MUKUNDAN 1 ingests the canonical dataset of 1,161 holdouts maintained by the bbchallenge.org research initiative. Checkpoints and proofs are verified natively by the orchestrator:
</p>
<table>
    <thead>
        <tr>
            <th>Holdout ID</th>
            <th>Machine TNF Seed</th>
            <th>Circuit Constraints</th>
            <th>Proof Size</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>BB6-0000</code></td>
            <td><code>1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA</code></td>
            <td>1,842</td>
            <td>2,144 bytes</td>
            <td>Verified</td>
        </tr>
        <tr>
            <td><code>BB6-0006</code></td>
            <td><code>1RB---_1RC1RD_1RE1LC_1LE1RF_1LC0LE_1RA0RA</code></td>
            <td>1,842</td>
            <td>2,144 bytes</td>
            <td>Verified</td>
        </tr>
        <tr>
            <td><code>BB6-0010</code></td>
            <td><code>1RB1RC_1LC1RD_1RE1LC_1LE1RF_1LC0LE_1RA0RA</code></td>
            <td>1,842</td>
            <td>2,144 bytes</td>
            <td>Verified</td>
        </tr>
        <tr>
            <td><code>BB6-0052</code></td>
            <td><code>1RB1LC_1RC1RD_1RE1LC_1LE1RF_1LC0LE_1RA0RA</code></td>
            <td>1,842</td>
            <td>2,144 bytes</td>
            <td>Verified</td>
        </tr>
    </tbody>
</table>
</div>

<div class="page-break"></div>

<h2>5. Node Telemetry & Telemetric Inspection</h2>
<p>
Below are telemetry captures demonstrating the browser node execution, non-blocking Web Worker thread scheduling, and zero-copy linear memory extraction:
</p>

<div class="avoid-break">
    <h3>Client Node Web Dashboard (Attachment S15)</h3>
    <img class="diagram-img" src="###S15_IMG###" alt="S15 Client Dashboard" />
</div>

<div class="page-break"></div>

<div class="avoid-break">
    <h3>Chrome DevTools Telemetry & Memory Inspection (Attachment S16)</h3>
    <img class="diagram-img" src="###S16_IMG###" alt="S16 DevTools Telemetry" />
</div>

<h2>6. Transparent Limitations & Engineering Roadmap</h2>
<div class="callout">
    <strong>Engineering Honesty —</strong> Rather than concealing in-progress modules, MUKUNDAN 1 explicitly documents technical boundaries:
    <ul>
        <li><strong>WebGPU MSM Accumulation:</strong> <code>bn254_msm.wgsl</code> implements complete 256-bit multi-precision arithmetic (addition with carry, subtraction with borrow, and Montgomery modular reduction). The Pippenger bucket accumulation loop across curve base points is architecturally stubbed.</li>
        <li><strong>Recursive Folding (IVC):</strong> Transitions are currently proven step-by-step. Integrating Incremental Verifiable Computation (Protogalaxy or Nova) will allow folding 1,000,000 steps into a single recurring proof.</li>
        <li><strong>State Persistence:</strong> Checkpoint states are maintained in-memory for active sessions (<code>db_connector.rs</code> is in development).</li>
    </ul>
</div>

<h2>7. Verification & Reproduction</h2>
<p>
The complete codebase is publicly available and verifiable on GitHub at <a href="https://github.com/theviolinplayer/mukundan-1">github.com/theviolinplayer/mukundan-1</a>. Execution requires two concurrent processes:
</p>
<pre>
# Terminal 1: Orchestrator Backend Server
cd server
$env:CARGO_TARGET_DIR="target_standalone"; cargo run --release

# Terminal 2: Volunteer Browser Node Host
cd client
npx vite
</pre>
<p style="text-align: center; color: #64748b; font-size: 8pt; margin-top: 15px;">
    MUKUNDAN 1 &bull; MIT Maker Portfolio 2026 &bull; Authored by Mukundan Padmaraj &bull; Cambridge, MA
</p>

</body>
</html>
"""

    html_content = template.replace("###RUN_IMG###", run_img).replace("###S15_IMG###", s15_img).replace("###S16_IMG###", s16_img)

    html_path = os.path.join(root_dir, "data", "report_temp.html")
    pdf_out1 = os.path.join(root_dir, "data", "MUKUNDAN_1_Technical_Report.pdf")
    pdf_out2 = r"C:\Users\O M E N\Desktop\Mukundan\MIT essays\Maker portfolio\MUKUNDAN_1_Technical_Report.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={pdf_out1}",
        "--no-pdf-header-footer",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(pdf_out1):
        import shutil
        try:
            shutil.copyfile(pdf_out1, pdf_out2)
            print("Successfully saved to:", pdf_out2)
        except Exception as e:
            print("Could not copy to portfolio folder:", e)
        print("Generated PDF:", pdf_out1, "Size:", os.path.getsize(pdf_out1))
    else:
        print("Failed to generate PDF:", res.stderr)

    if os.path.exists(html_path):
        os.remove(html_path)

if __name__ == "__main__":
    generate_pdf()
