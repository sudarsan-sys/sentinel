from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    def __init__(self, camera_id: str, source_uri: str, config: dict):
        self.camera_id = camera_id
        self.source_uri = source_uri
        self.config = config
        self.is_connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the camera source."""
        pass

    @abstractmethod
    def get_stream_uri(self) -> str:
        """Return the normalized RTSP URI that MediaMTX will use/expose."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the connection is still alive."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect and clean up resources."""
        pass
