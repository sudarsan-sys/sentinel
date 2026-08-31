import time
import os
import yaml
import psycopg2
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from adapters.adapter_factory import get_adapter

def get_db_connection():
    db_url = os.environ.get("DB_URL", "postgresql://postgres:postgres@localhost:5432/sentinel")
    return psycopg2.connect(db_url)

def monitor_loop():
    config_path = os.path.join(os.path.dirname(__file__), "../config/cameras.yaml")
    adapter_config_path = os.path.join(os.path.dirname(__file__), "../config/adapter_config.yaml")

    with open(config_path) as f:
        camera_config = yaml.safe_load(f)
        
    with open(adapter_config_path) as f:
        adapter_config = yaml.safe_load(f)

    # Initialize adapters
    adapters = []
    for cam in camera_config["cameras"]:
        adapter = get_adapter(cam, adapter_config)
        adapter.connect()
        adapters.append(adapter)

    conn = get_db_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        while True:
            for adapter in adapters:
                is_healthy = adapter.health_check()
                status = "online" if is_healthy else "offline"
                
                # Update DB
                cursor.execute(
                    "UPDATE cameras SET status = %s WHERE id = %s",
                    (status, adapter.camera_id)
                )
                print(f"Checked {adapter.camera_id}: {status}")
            
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        for adapter in adapters:
            adapter.disconnect()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    monitor_loop()
