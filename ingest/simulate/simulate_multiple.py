import yaml
import subprocess
import os
import time

def main():
    config_path = os.path.join(os.path.dirname(__file__), "../config/cameras.yaml")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)

    processes = []
    script_path = os.path.join(os.path.dirname(__file__), "ffmpeg_simulate_camera.sh")

    try:
        for cam in config["cameras"]:
            cam_id = cam["id"]
            # The source URI in yaml is relative to ingest/config, adjust it to be relative to ingest/simulate
            # Or just pass the absolute/resolved path
            source_uri = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "config", cam["source_uri"]))
            print(f"Starting simulation for {cam_id}...")
            
            p = subprocess.Popen(["bash", script_path, cam_id, source_uri])
            processes.append(p)
            
        print("All simulated cameras started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Shutting down simulated cameras...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
