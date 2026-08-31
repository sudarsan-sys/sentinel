from .base_adapter import BaseAdapter

class RTSPOnvifAdapter(BaseAdapter):
    def connect(self) -> bool:
        # In a real scenario, this might verify the ONVIF credentials or probe the RTSP stream.
        # For the prototype, we assume the URI is reachable.
        self.is_connected = True
        return True

    def get_stream_uri(self) -> str:
        # We simply pass the source URI through, assuming it's already an RTSP link 
        # (or for our simulation, it's the video file path to be ffmpeg'd).
        return self.source_uri

    def health_check(self) -> bool:
        return self.is_connected

    def disconnect(self) -> None:
        self.is_connected = False
