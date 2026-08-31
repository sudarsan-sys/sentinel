from .rtsp_onvif_adapter import RTSPOnvifAdapter
from .mock_vendor_adapter import MockVendorAdapter

def get_adapter(camera_config: dict, global_config: dict):
    """
    Factory to instantiate the correct adapter based on the camera configuration.
    """
    source_type = camera_config.get("source_type")
    camera_id = camera_config.get("id")
    source_uri = camera_config.get("source_uri")
    
    if source_type == "rtsp_onvif":
        return RTSPOnvifAdapter(camera_id, source_uri, global_config)
    elif source_type == "mock_vendor":
        return MockVendorAdapter(camera_id, source_uri, global_config)
    elif source_type == "sandbox":
        from .sandbox_adapter import SandboxAdapter
        return SandboxAdapter(camera_id, source_uri, global_config)
    else:
        raise ValueError(f"Unknown source_type: {source_type} for camera {camera_id}")

if __name__ == "__main__":
    # Quick sanity check
    import yaml
    with open("../config/cameras.yaml") as f:
        config = yaml.safe_load(f)
    
    with open("../config/adapter_config.yaml") as f:
        adapter_config = yaml.safe_load(f)

    for cam in config["cameras"]:
        adapter = get_adapter(cam, adapter_config)
        print(f"Instantiated {type(adapter).__name__} for {cam['id']}")
