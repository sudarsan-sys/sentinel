# Sample Videos

This directory contains simulated camera feeds for the Sentinel prototype.

We use simple looping videos to test the ingest pipeline.
To generate a basic test video using ffmpeg:
`ffmpeg -f lavfi -i testsrc=duration=10:size=1280x720:rate=30 sample1.mp4`

Drop your new files in here and update `ingest/config/cameras.yaml` to point to them.
