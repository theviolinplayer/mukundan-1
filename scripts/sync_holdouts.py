import json
import requests
import os

# Ground Zero: The 1,161 holdout list for BB(6) as of March 2026
URL = "https://wiki.bbchallenge.org/w/images/2/2a/BB6_holdouts_1161.txt"

def sync():
    # Get the absolute path of the directory where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level and then into the 'data' folder
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, "holdouts.json")
    
    print(f"Downloading BB(6) holdouts from {URL}...")
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Network Error: {e}")
        return

    # Filter out empty lines and comments
    raw_seeds = [line.strip() for line in response.text.split('\n') if line.strip() and not line.startswith('#')]
    
    holdouts = []
    for index, seed in enumerate(raw_seeds):
        holdouts.append({
            "id": f"BB6-{index:04d}",
            "seed": seed,
            "status": "undecided"
        })
    
    # Write with indentation for readability (Engineering Notebook requirement)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"holdouts": holdouts}, f, indent=2)
        f.flush() # Force write to disk
        os.fsync(f.fileno()) # Deep system-level flush
        
    print(f"Verification: {len(holdouts)} machines saved.")
    print(f"Full Path: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    sync()