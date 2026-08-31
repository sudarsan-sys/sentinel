from .base_adapter import BaseAdapter

class MockVendorAdapter(BaseAdapter):
    def connect(self) -> bool:
        # Simulate connecting to a proprietary SDK (like Hikvision ISAPI or Dahua)
        self.is_connected = True
        return True

    def get_stream_uri(self) -> str:
        # Simulate asking the SDK for an RTSP endpoint that it internally manages
        # For simulation purposes, it acts similarly to the RTSP adapter by providing the URI.
        return self.source_uri

    def health_check(self) -> bool:
        # Simulate checking the SDK connection status
        return self.is_connected

    def disconnect(self) -> None:
        # Simulate tearing down the SDK connection
        self.is_connected = False
