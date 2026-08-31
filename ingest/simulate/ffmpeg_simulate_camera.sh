#!/bin/bash
# simulate/ffmpeg_simulate_camera.sh
# Usage: ./ffmpeg_simulate_camera.sh <camera_id> <video_file_path>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <camera_id> <video_file_path>"
    exit 1
fi

CAMERA_ID=$1
VIDEO_FILE=$2

MEDIAMTX_URL="rtsp://localhost:8554/${CAMERA_ID}"

echo "Starting stream for ${CAMERA_ID} using ${VIDEO_FILE} to ${MEDIAMTX_URL}"

# Loop the video infinitely and stream it to MediaMTX
ffmpeg -re -stream_loop -1 -i "${VIDEO_FILE}" -c copy -f rtsp "${MEDIAMTX_URL}"
