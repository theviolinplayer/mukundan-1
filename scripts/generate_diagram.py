from PIL import Image, ImageDraw, ImageFont
import os

diagram_text = """+---------------------------------------------------------------------------------------------------------+
|                                    MUKUNDAN 1: RUNTIME EXECUTION MECHANISM                              |
|               Multi-node Universal Kernel for Unified Non-halting Distributed Automata Networks         |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [TERMINAL 1: Orchestrator Server]                      [TERMINAL 2: Client Node Host]                  |
|  $ cd server                                            $ cd client                                     |
|  $ $env:CARGO_TARGET_DIR="target_standalone"            $ npx vite                                      |
|    cargo run --release                                                                                  |
|                                                                                                         |
|  +--------------------------------------+               +--------------------------------------+        |
|  |          Rust Server (Warp)          |               |           Vite Dev Server            |        |
|  |  * Ingests 1,161 BB(6) Holdouts      |               |  * Serves client frontend bundle     |        |
|  |  * Binds to http://0.0.0.0:3030      |               |  * Hosts on http://localhost:5173    |        |
|  |  * Dispatches unassigned machines    |               |  * Loads WASM linear memory bridge   |        |
|  |  * Verifies incoming ZK-SNARK proofs |               +------------------+-------------------+        |
|  +------------------+-------------------+                                  |                            |
|                     ^                                                      | Serves static assets       |
|                     |                                                      v                            |
|                     | WebSocket / HTTP REST         +------------------------------------------+        |
|                     | (Port 3030)                   |          VOLUNTEER BROWSER NODE          |        |
|                     |                               |         (Any Modern Web Browser)         |        |
|                     |                               +------------------------------------------+        |
|                     | 1. GET /api/v1/work           | 1. User clicks:                          |        |
|                     |    -> Receives holdout seed   |    "INITIALIZE VERIFIABLE WORKER"        |        |
|                     |                               | 2. Spawns secure Web Worker thread       |        |
|                     |                               | 3. Simulates in WebAssembly (WASM)       |        |
|                     |                               | 4. Solves Noir execution witness         |        |
|                     | 2. POST /api/v1/checkpoint    | 5. WebGPU shader accelerates MSM         |        |
|                     |    -> Submits state + SNARK   | 6. Generates constant-size ZK proof      |        |
|                     +-------------------------------+------------------------------------------+        |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+"""

lines = diagram_text.split('\n')
font_size = 18
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', font_size)

# Dimensions
padding_x = 40
padding_y = 40

# Compute accurate character widths using font.getbbox
sample_bbox = font.getbbox("A")
char_width = sample_bbox[2] - sample_bbox[0]
line_height = int(font_size * 1.5)

max_line_len = max(len(l) for l in lines)
img_width = int(max_line_len * char_width + padding_x * 2)
img_height = int(len(lines) * line_height + padding_y * 2)

img = Image.new('RGB', (img_width, img_height), (13, 17, 23))
draw = ImageDraw.Draw(img)

y = padding_y
for idx, line in enumerate(lines):
    color = (201, 209, 217)  # default text
    if idx == 1:
        color = (88, 166, 255)  # Title cyan/blue
    elif idx == 2:
        color = (139, 148, 158)  # Subtitle gray
    elif '[TERMINAL 1' in line or '[TERMINAL 2' in line:
        color = (210, 153, 34)  # Orange terminal headers
    elif line.strip().startswith('$'):
        color = (126, 231, 135)  # Command green
    elif 'VOLUNTEER BROWSER NODE' in line:
        color = (218, 112, 214)  # Orchid browser node
    elif 'Rust Server' in line or 'Vite Dev Server' in line:
        color = (121, 192, 255)  # Light blue
    elif '1. GET' in line or '2. POST' in line:
        color = (240, 136, 62)  # Orange API endpoints
    elif set(line.strip()).issubset({'+', '-', '|', ' '}):
        color = (68, 76, 86)  # Dark border
        
    draw.text((padding_x, y), line, font=font, fill=color)
    y += line_height

out1 = r'c:\Users\O M E N\Desktop\Mukundan\Proof of Work\mukundan-1\data\running_mechanism.png'
out2 = r'C:\Users\O M E N\Desktop\Mukundan\MIT essays\Maker portfolio\running_mechanism.png'

os.makedirs(os.path.dirname(out1), exist_ok=True)
img.save(out1, 'PNG')
try:
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    img.save(out2, 'PNG')
except Exception as e:
    pass

print("Successfully generated:", out1)
