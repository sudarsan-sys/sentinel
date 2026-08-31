import time
import threading
import logging
import sys

from ingest.adapters.sandbox_adapter import SandboxAdapter

# Setup basic logging to see the output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger("backoff_test")

def restore_url_after_delay(adapter, valid_url, delay):
    time.sleep(delay)
    logger.info(f"--- THREAD: Restoring valid URL {valid_url} after {delay} seconds ---")
    adapter.source_uri = valid_url

def main():
    valid_url = "rtsp://live.corp8.cloud:8554/stream/6"
    bad_url = "rtsp://live.corp8.cloud:8554/stream/invalid_stream_999"
    
    # Initialize adapter with valid URL
    adapter = SandboxAdapter(camera_id="test_cam", source_uri=valid_url, config={'max_backoff_seconds': 30})
    
    logger.info("1. Connecting to valid stream...")
    success = adapter.connect()
    if not success:
        logger.error("Failed to connect to initial valid stream.")
        return
        
    logger.info("2. Connection successful. Checking health...")
    adapter.health_check()
    
    logger.info("3. Simulating dropped connection by pointing to a bad URL and forcing disconnect...")
    adapter.disconnect()
    adapter.source_uri = bad_url
    
    # Start a background thread to restore the valid URL after 15 seconds.
    # This will allow us to observe multiple backoff attempts (2s, 4s, 8s) before it recovers.
    threading.Thread(target=restore_url_after_delay, args=(adapter, valid_url, 15), daemon=True).start()
    
    logger.info("4. Attempting to reconnect. This should fail initially and trigger the backoff sequence...")
    # This will block and backoff until the thread restores the good URL
    adapter.connect()
    
    logger.info("5. Reconnect succeeded! Stream is back online.")
    adapter.disconnect()

if __name__ == "__main__":
    main()
