import os
import time
import logging
import requests
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://live.corp8.cloud/api/ingest"

def get_db_connection():
    db_url = os.environ.get("DB_URL", "postgresql://postgres:postgres@localhost:5432/sentinel")
    return psycopg2.connect(db_url)

def sync_catalogue():
    """
    Polls the Sentinel Sandbox catalogue API and syncs cameras into the database.
    Runs periodically.
    """
    logger.info(f"Fetching camera catalogue from {API_URL}...")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        camera_list = data.get("cameras", data) if isinstance(data, dict) else data
    except Exception as e:
        logger.error(f"Failed to fetch catalogue: {e}")
        return

    logger.info(f"Found {len(camera_list)} cameras in the sandbox catalogue.")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for cam in camera_list:
            # Add 'sb_' prefix to avoid conflicts with our simulated cam1/cam2 IDs,
            # or just use the ID as provided by the sandbox.
            cam_id = f"sb_{cam['id']}" 
            
            # The API provides 'rtsp_url', 'webrtc_url', 'hls_live_url'
            # We map this to source_type = 'sandbox'
            
            cursor.execute("""
                INSERT INTO cameras (id, name, source_type, department, vendor, lat, lon, webrtc_url, hls_url, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    source_type = EXCLUDED.source_type,
                    department = EXCLUDED.department,
                    vendor = EXCLUDED.vendor,
                    webrtc_url = EXCLUDED.webrtc_url,
                    hls_url = EXCLUDED.hls_url,
                    status = EXCLUDED.status
            """, (
                cam_id, 
                cam.get("name", f"Sandbox {cam['id']}"), 
                "sandbox", 
                cam.get("location", "Sandbox Grid"), 
                cam.get("codec", "unknown"), 
                0.0, 
                0.0,
                cam.get("webrtc_url"),
                cam.get("hls_live_url"),
                'online' if cam.get("live") else 'offline'
            ))
            
        conn.commit()
        logger.info("Catalogue successfully synced to database.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error during sync: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    while True:
        sync_catalogue()
        time.sleep(60)
