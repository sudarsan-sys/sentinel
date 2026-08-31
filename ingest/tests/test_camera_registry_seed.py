import pytest
from unittest.mock import patch, MagicMock
from ingest.registry.camera_registry_seed import seed_database

@patch('ingest.registry.camera_registry_seed.get_db_connection')
@patch('ingest.registry.camera_registry_seed.open')
@patch('ingest.registry.camera_registry_seed.yaml.safe_load')
def test_seed_database(mock_yaml_load, mock_open, mock_db_conn):
    # Mock the yaml config
    mock_yaml_load.return_value = {
        "cameras": [
            {
                "id": "cam1",
                "source_type": "rtsp_onvif",
                "department": "Traffic Police",
                "vendor": "Generic RTSP",
                "lat": 23.0,
                "lon": 72.0
            }
        ]
    }
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    # Run the seed function
    seed_database()

    # Verify table creation was called
    assert mock_cursor.execute.call_count == 2 # CREATE TABLE, then INSERT
    
    # Verify the insert was called with right arguments
    insert_call_args = mock_cursor.execute.call_args_list[1][0]
    assert "INSERT INTO cameras" in insert_call_args[0]
    assert insert_call_args[1] == ("cam1", "Camera cam1", "rtsp_onvif", "Traffic Police", "Generic RTSP", 23.0, 72.0)
    
    mock_conn.commit.assert_called_once()
