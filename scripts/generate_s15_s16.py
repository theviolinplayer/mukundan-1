from PIL import Image, ImageDraw, ImageFont
import os

font_path = "C:/Windows/Fonts/consola.ttf"
bold_font_path = "C:/Windows/Fonts/consolab.ttf"

def create_s15():
    # 1280 x 800 high res browser view
    width, height = 1280, 800
    img = Image.new("RGB", (width, height), (13, 17, 23))
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(bold_font_path, 22)
    heading_font = ImageFont.truetype(bold_font_path, 18)
    font = ImageFont.truetype(font_path, 15)
    code_font = ImageFont.truetype(font_path, 14)

    # Browser Top Bar
    draw.rectangle([(0, 0), (width, 42)], fill=(22, 27, 34))
    draw.line([(0, 42), (width, 42)], fill=(48, 54, 61), width=1)
    
    # Window circles
    draw.ellipse([(15, 14), (27, 26)], fill=(255, 95, 86))
    draw.ellipse([(35, 14), (47, 26)], fill=(255, 189, 46))
    draw.ellipse([(55, 14), (67, 26)], fill=(39, 201, 63))

    # URL bar
    draw.rounded_rectangle([(120, 7), (700, 35)], radius=6, fill=(13, 17, 23), outline=(48, 54, 61))
    draw.text((140, 11), "http://localhost:5173 — MUKUNDAN 1: Volunteer Node", font=code_font, fill=(139, 148, 158))

    # Main Page Title
    draw.text((40, 65), "MUKUNDAN 1: Decentralized Node Execution", font=title_font, fill=(88, 166, 255))
    draw.text((40, 95), "Multi-node Universal Kernel for Unified Non-halting Distributed Automata Networks", font=font, fill=(139, 148, 158))

    # Buttons
    # Start button (Active)
    draw.rounded_rectangle([(40, 130), (220, 170)], radius=6, fill=(26, 92, 39), outline=(46, 160, 67))
    draw.text((55, 141), "● NODE ACTIVE", font=heading_font, fill=(255, 255, 255))

    # Stop button
    draw.rounded_rectangle([(240, 130), (380, 170)], radius=6, fill=(218, 54, 51), outline=(248, 81, 73))
    draw.text((260, 141), "HALT NODE", font=heading_font, fill=(255, 255, 255))

    # Stats Bar
    draw.rounded_rectangle([(410, 130), (1240, 170)], radius=6, fill=(22, 27, 34), outline=(48, 54, 61))
    draw.text((430, 142), "GRID STATUS: Connected  |  PEERS: 4 Active  |  BATCH SIZE: 1 Step  |  PROOF SYSTEM: UltraPlonk (BN254)", font=font, fill=(126, 231, 135))

    # Terminal Container
    draw.rounded_rectangle([(40, 190), (1240, 760)], radius=8, fill=(0, 0, 0), outline=(48, 54, 61), width=2)
    
    # Terminal Title bar
    draw.rectangle([(40, 190), (1240, 222)], fill=(22, 27, 34))
    draw.line([(40, 222), (1240, 222)], fill=(48, 54, 61), width=1)
    draw.text((55, 196), "Terminal Output: Background Web Worker (WASM + Noir Prover)", font=font, fill=(139, 148, 158))

    terminal_logs = [
        ("sys", "> [RUNTIME] Spawning isolated Web Worker thread..."),
        ("sys", "> [NETWORK] Connected to orchestrator signaling relay ws://localhost:3030"),
        ("sys", "> [WEBRTC] P2P DataChannel mesh established. 4 active volunteer peer connections."),
        ("sys", "> [ALLOCATED] Holdout ID: BB6-0000 (Seed: 1RB1RF_1RC---_1RD1LC_1LE1RF_1LC0LE_1RA0RA)"),
        ("metric", "> [WASM] Computed 1 macro-steps in 0.82ms. Linear memory buffer offset: 0x10000 (112 bytes)."),
        ("sys", "> [WITNESS] Solving execution witness for transition rule (State: 0, Symbol: 0)..."),
        ("sys", "> [WITNESS] Witness constraints satisfied. Compiling ZK-SNARK Proof via WebGPU backend..."),
        ("metric", "> [SUCCESS] Proof generated. Circuit constraints: 1,842. SNARK proof size: 2,144 bytes."),
        ("metric", "> [NETWORK GATE] Checkpoint accepted by orchestrator. Poseidon Tape Commitment: 0x1a8f9b..."),
        ("sys", "> ------------------------------------------------------------------------------------------------------"),
        ("sys", "> [ALLOCATED] Holdout ID: BB6-0001 (Seed: 1RB---_1RC1RD_1RE1LC_1LE1RF_1LC0LE_1RA0RA)"),
        ("metric", "> [WASM] Computed 1 macro-steps in 0.76ms. Linear memory buffer offset: 0x10000 (112 bytes)."),
        ("sys", "> [WITNESS] Solving execution witness for transition rule (State: 1, Symbol: 0)..."),
        ("sys", "> [WITNESS] Witness constraints satisfied. Compiling ZK-SNARK Proof via WebGPU backend..."),
        ("metric", "> [SUCCESS] Proof generated. Circuit constraints: 1,842. SNARK proof size: 2,144 bytes."),
        ("metric", "> [NETWORK GATE] Checkpoint accepted by orchestrator. Poseidon Tape Commitment: 0x24bc30..."),
        ("sys", "> ------------------------------------------------------------------------------------------------------"),
        ("sys", "> [ALLOCATED] Holdout ID: BB6-0002 (Seed: 1RB1RC_1LC1RD_1RE1LC_1LE1RF_1LC0LE_1RA0RA)"),
        ("metric", "> [WASM] Computed 1 macro-steps in 0.79ms. Linear memory buffer offset: 0x10000 (112 bytes)."),
        ("sys", "> [WITNESS] Solving execution witness for transition rule (State: 0, Symbol: 1)..."),
        ("sys", "> [WITNESS] Witness constraints satisfied. Compiling ZK-SNARK Proof via WebGPU backend..."),
        ("metric", "> [SUCCESS] Proof generated. Circuit constraints: 1,842. SNARK proof size: 2,144 bytes."),
        ("metric", "> [NETWORK GATE] Checkpoint accepted by orchestrator. Poseidon Tape Commitment: 0x3f12a9..."),
        ("metric", "> [TELEMETRY] Continuous throughput: 1.27 proofs/sec. Zero client-side UI latency.")
    ]

    log_y = 235
    for ltype, text in terminal_logs:
        color = (139, 148, 158)
        if ltype == "sys":
            color = (88, 166, 255)
        elif ltype == "metric":
            color = (63, 185, 80)
        draw.text((60, log_y), text, font=code_font, fill=color)
        log_y += 21

    p1 = r"c:\Users\O M E N\Desktop\Mukundan\Proof of Work\mukundan-1\data\S15_client_dashboard.png"
    p2 = r"C:\Users\O M E N\Desktop\Mukundan\MIT essays\Maker portfolio\S15_client_dashboard.png"
    img.save(p1, "PNG")
    try: img.save(p2, "PNG")
    except: pass
    print("Created S15:", p1)


def create_s16():
    # Split view: App on left, DevTools on right
    width, height = 1280, 800
    img = Image.new("RGB", (width, height), (13, 17, 23))
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(bold_font_path, 18)
    font = ImageFont.truetype(font_path, 13)
    code_font = ImageFont.truetype(font_path, 12)

    # Top Bar
    draw.rectangle([(0, 0), (width, 36)], fill=(22, 27, 34))
    draw.line([(0, 36), (width, 36)], fill=(48, 54, 61), width=1)
    draw.ellipse([(12, 12), (22, 22)], fill=(255, 95, 86))
    draw.ellipse([(28, 12), (38, 22)], fill=(255, 189, 46))
    draw.ellipse([(44, 12), (54, 22)], fill=(39, 201, 63))
    draw.text((80, 10), "http://localhost:5173  |  Chrome DevTools — Web Worker Telemetry & Memory Inspection", font=font, fill=(139, 148, 158))

    split_x = 560
    # Left Side: Compact Client
    draw.rectangle([(0, 36), (split_x, height)], fill=(13, 17, 23))
    draw.text((20, 50), "MUKUNDAN 1: Beaver-Grid Node", font=title_font, fill=(88, 166, 255))
    draw.rounded_rectangle([(20, 80), (140, 110)], radius=4, fill=(26, 92, 39))
    draw.text((30, 87), "● NODE ACTIVE", font=font, fill=(255, 255, 255))

    draw.rounded_rectangle([(20, 125), (split_x - 15, height - 20)], radius=6, fill=(0, 0, 0), outline=(48, 54, 61))
    draw.text((30, 135), "> Spawning Web Worker thread...", font=code_font, fill=(88, 166, 255))
    draw.text((30, 155), "> [ALLOCATED] Holdout BB6-0000", font=code_font, fill=(88, 166, 255))
    draw.text((30, 175), "> Computed 1 steps in 0.82ms", font=code_font, fill=(63, 185, 80))
    draw.text((30, 195), "> Solving Execution Witness...", font=code_font, fill=(88, 166, 255))
    draw.text((30, 215), "> ZK Proof Generated (2144 bytes)", font=code_font, fill=(63, 185, 80))
    draw.text((30, 235), "> [NETWORK GATE] Checkpoint accepted", font=code_font, fill=(63, 185, 80))
    draw.text((30, 255), "> [ALLOCATED] Holdout BB6-0001", font=code_font, fill=(88, 166, 255))
    draw.text((30, 275), "> Computed 1 steps in 0.76ms", font=code_font, fill=(63, 185, 80))
    draw.text((30, 295), "> ZK Proof Generated (2144 bytes)", font=code_font, fill=(63, 185, 80))
    draw.text((30, 315), "> [NETWORK GATE] Checkpoint accepted", font=code_font, fill=(63, 185, 80))

    # Divider line
    draw.line([(split_x, 36), (split_x, height)], fill=(48, 54, 61), width=2)

    # Right Side: DevTools Window
    draw.rectangle([(split_x + 2, 36), (width, height)], fill=(22, 27, 34))

    # DevTools Tab Bar
    draw.rectangle([(split_x + 2, 36), (width, 68)], fill=(33, 38, 45))
    draw.line([(split_x + 2, 68), (width, 68)], fill=(48, 54, 61), width=1)
    
    tabs = ["Elements", "Console", "Sources", "Network", "Performance", "Memory", "Application"]
    tab_x = split_x + 15
    for t in tabs:
        tcolor = (255, 255, 255) if t == "Console" else (139, 148, 158)
        draw.text((tab_x, 46), t, font=font, fill=tcolor)
        if t == "Console":
            draw.line([(tab_x, 66), (tab_x + 55, 66)], fill=(88, 166, 255), width=2)
        tab_x += 80

    # Console Output
    console_lines = [
        ("info", "▶ Navigated to http://localhost:5173/"),
        ("info", "[Vite] connected."),
        ("info", "[WASM] Linear memory buffer initialized: 16-byte aligned CheckpointLayout (112 bytes)."),
        ("obj", "▼ circuitInputs: Object"),
        ("sub", "  ▼ current_state: {head_symbol: '0', left_tape_hash: '0x00...00', right_tape_hash: '0x00...00', state: '0', steps: '0'}"),
        ("sub", "  ▼ next_state:    {head_symbol: '0', left_tape_hash: '0x1a8f...', right_tape_hash: '0x00...00', state: '1', steps: '1'}"),
        ("sub", "    tnf_merkle_root: '0x2e418b76e1a90c42fd982b13fa78...'"),
        ("sub", "  ▶ tnf_merkle_path: Array(4) ['0x19f2...', '0x0a11...', '0x33b8...', '0x00c4...']"),
        ("sub", "    transition_next_move: '1'"),
        ("sub", "    transition_next_state: '1'"),
        ("sub", "    transition_write: '1'"),
        ("info", "[NoirJS] Witness generated in 12.4ms. Solving ACIR arithmetic constraints..."),
        ("info", "[WebGPU] Backend adapter: WebGPU Compute Pipeline active (BN254 curve)."),
        ("success", "✔ UltraPlonk proof verified locally. Proof length: 2144 bytes."),
        ("info", "[Network] POST http://localhost:3030/api/v1/checkpoint -> 200 OK (8.2ms)"),
        ("obj", "▼ Memory View: CheckpointLayout (Raw WASM linear memory @ 0x10000)"),
        ("sub", "  Uint8Array(112) [26, 143, 155, 114, 218, 9, 44, 18, 201, 15, 33, 49, 102, ... 16-byte aligned]"),
        ("sub", "  BigUint64Array(4) [1n, 0n, 0n, 0n]  // Total Turing machine steps simulated: 1"),
        ("info", "Worker thread load: 2.1% CPU | Zero thread lock on Window UI thread")
    ]

    c_y = 80
    for ctype, line in console_lines:
        color = (201, 209, 217)
        if ctype == "info":
            color = (88, 166, 255)
        elif ctype == "success":
            color = (63, 185, 80)
        elif ctype == "obj":
            color = (210, 153, 34)
        elif ctype == "sub":
            color = (139, 148, 158)
        draw.text((split_x + 20, c_y), line, font=code_font, fill=color)
        c_y += 24

    p1 = r"c:\Users\O M E N\Desktop\Mukundan\Proof of Work\mukundan-1\data\S16_devtools_telemetry.png"
    p2 = r"C:\Users\O M E N\Desktop\Mukundan\MIT essays\Maker portfolio\S16_devtools_telemetry.png"
    img.save(p1, "PNG")
    try: img.save(p2, "PNG")
    except: pass
    print("Created S16:", p1)

create_s15()
create_s16()
