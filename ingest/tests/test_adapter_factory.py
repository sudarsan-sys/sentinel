import pytest
from ingest.adapters.adapter_factory import get_adapter
from ingest.adapters.rtsp_onvif_adapter import RTSPOnvifAdapter
from ingest.adapters.mock_vendor_adapter import MockVendorAdapter

def test_get_rtsp_adapter():
    config = {"id": "cam1", "source_type": "rtsp_onvif", "source_uri": "test.mp4"}
    adapter = get_adapter(config, {})
    assert isinstance(adapter, RTSPOnvifAdapter)
    assert adapter.camera_id == "cam1"

def test_get_mock_adapter():
    config = {"id": "cam2", "source_type": "mock_vendor", "source_uri": "test2.mp4"}
    adapter = get_adapter(config, {})
    assert isinstance(adapter, MockVendorAdapter)

def test_invalid_adapter():
    config = {"id": "cam3", "source_type": "invalid_type", "source_uri": "test3.mp4"}
    with pytest.raises(ValueError, match="Unknown source_type"):
        get_adapter(config, {})
