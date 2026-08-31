import os
import time
import logging

# [DO] Force RTSP over TCP. UDP is accepted but fails across NAT/firewalls.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

import cv2
from .base_adapter import BaseAdapter

logger = logging.getLogger(__name__)

class SandboxAdapter(BaseAdapter):
    def __init__(self, camera_id: str, source_uri: str, config: dict):
        super().__init__(camera_id, source_uri, config)
        self.cap = None
        self._is_connected = False
        
        # Pull max backoff from config if present, default to 30s
        self.max_backoff = self.config.get('max_backoff_seconds', 30)

    def connect(self) -> bool:
        """
        Connects to the RTSP stream with exponential backoff.
        [DO] Reconnect automatically, with backoff (start at ~2s, cap at ~30s).
        """
        backoff = 2
        while not self._is_connected:
            logger.info(f"[{self.camera_id}] Attempting connection to {self.source_uri}...")
            
            # [DON'T] Treat decode warnings at join as fatal.
            # cv2.VideoCapture handles this internally by logging warnings and not crashing.
            self.cap = cv2.VideoCapture(self.source_uri, cv2.CAP_FFMPEG)
            
            if self.cap.isOpened():
                logger.info(f"[{self.camera_id}] Successfully connected.")
                self._is_connected = True
                return True
            
            logger.warning(f"[{self.camera_id}] Connection failed. Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff = min(backoff * 2, self.max_backoff)
            
        return False

    def get_stream_uri(self) -> str:
        # In a real ingest, we might restream it, but for Sentinel sandbox,
        # downstream models can connect directly to the RTSP URL.
        # This returns the sandbox URL.
        return self.source_uri

    def health_check(self) -> bool:
        """
        Check if the connection is alive by trying to grab a frame.
        """
        if not self._is_connected or self.cap is None or not self.cap.isOpened():
            logger.warning(f"[{self.camera_id}] Health check failed: Not connected.")
            self._is_connected = False
            return False
            
        # Try to grab a frame without decoding it fully just to check health
        # [DON'T] Assume constant frame rate or crash on inter-frame gaps.
        ok = self.cap.grab()
        if not ok:
            logger.warning(f"[{self.camera_id}] Frame grab failed. Stream may have disconnected.")
            self._is_connected = False
            return False
            
        return True

    def read_frame_with_pts(self):
        """
        Reads a frame and its corresponding PTS.
        
        [IMPORTANT - For Module 2 (Edge-AI)]:
        [DON'T] Trust the reported frame rate (CAP_PROP_FPS).
        [DO] Drive all timing from PTS, never from arrival time.
        
        This method serves as the blueprint for how Module 2 should consume frames.
        """
        if not self._is_connected or self.cap is None:
            return False, None, None
            
        ok, frame = self.cap.read()
        if not ok:
            # Stream drop or scene cut point
            return False, None, None
            
        # Actual PTS in milliseconds
        pts_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        
        return True, frame, pts_ms

    def disconnect(self) -> None:
        if self.cap is not None:
            self.cap.release()
        self._is_connected = False
        logger.info(f"[{self.camera_id}] Disconnected.")
