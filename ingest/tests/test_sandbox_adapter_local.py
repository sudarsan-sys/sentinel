import time
import threading
import logging
import sys
import os
import subprocess

from ingest.adapters.sandbox_adapter import SandboxAdapter

# Setup basic logging to see the output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger("backoff_test")

def main():
    # We will test against our own local MediaMTX since live.corp8.cloud:8554 is unreachable over the network
    valid_url = "rtsp://mediamtx:8554/cam1"
    
    # Initialize adapter with valid URL
    adapter = SandboxAdapter(camera_id="test_cam", source_uri=valid_url, config={'max_backoff_seconds': 30})
    
    logger.info("1. Connecting to valid stream...")
    success = adapter.connect()
    if not success:
        logger.error("Failed to connect to initial valid stream. Make sure docker-compose is running and ffmpeg_simulate_camera is streaming cam1!")
        return
        
    logger.info("2. Connection successful. Reading frames to verify PTS...")
    
    for _ in range(5):
        ok, frame, pts = adapter.read_frame_with_pts()
        if ok:
            logger.info(f"Read frame! PTS: {pts} ms")
        else:
            logger.warning("Frame read failed.")
        time.sleep(0.05)
        
    logger.info("3. Simulating dropped connection by forcing disconnect and triggering backoff...")
    
    # Simulate a mid-stream drop by just failing the health check manually and calling connect again
    adapter.disconnect()
    
    # To truly simulate an unreachable host for the backoff test, we point it to a dead port on localhost
    adapter.source_uri = "rtsp://mediamtx:8559/cam1"
    
    # Let's intercept the log and run the loop a few times
    adapter.connect()

if __name__ == "__main__":
    main()
