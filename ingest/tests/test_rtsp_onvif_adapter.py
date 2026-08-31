from ingest.adapters.rtsp_onvif_adapter import RTSPOnvifAdapter

def test_rtsp_adapter_uri():
    adapter = RTSPOnvifAdapter("cam1", "rtsp://10.0.0.1/stream", {})
    assert adapter.get_stream_uri() == "rtsp://10.0.0.1/stream"

def test_rtsp_adapter_connection():
    adapter = RTSPOnvifAdapter("cam1", "rtsp://10.0.0.1/stream", {})
    assert adapter.connect() is True
    assert adapter.health_check() is True
    adapter.disconnect()
    assert adapter.health_check() is False
