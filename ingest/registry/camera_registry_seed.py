import yaml
import os
import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    # Use environment variable or fallback to default
    db_url = os.environ.get("DB_URL", "postgresql://postgres:postgres@localhost:5432/sentinel")
    return psycopg2.connect(db_url)

def seed_database():
    config_path = os.path.join(os.path.dirname(__file__), "../config/cameras.yaml")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Stub for the table creation (normally defined in contracts/database.sql)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cameras (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            source_type VARCHAR,
            department VARCHAR,
            vendor VARCHAR,
            lat DOUBLE PRECISION,
            lon DOUBLE PRECISION,
            webrtc_url VARCHAR,
            hls_url VARCHAR,
            status VARCHAR DEFAULT 'offline'
        )
    """)

    for cam in config["cameras"]:
        cursor.execute("""
            INSERT INTO cameras (id, name, source_type, department, vendor, lat, lon, webrtc_url, hls_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'online')
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                source_type = EXCLUDED.source_type,
                department = EXCLUDED.department,
                vendor = EXCLUDED.vendor,
                lat = EXCLUDED.lat,
                lon = EXCLUDED.lon,
                webrtc_url = EXCLUDED.webrtc_url,
                hls_url = EXCLUDED.hls_url
        """, (
            cam["id"], 
            f"Camera {cam['id']}", 
            cam["source_type"], 
            cam["department"], 
            cam["vendor"], 
            cam.get("lat"), 
            cam.get("lon"),
            cam.get("webrtc_url"),
            cam.get("hls_url")
        ))
        print(f"Seeded {cam['id']} into the database.")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_database()
