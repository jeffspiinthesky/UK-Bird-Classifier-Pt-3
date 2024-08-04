#!/bin/bash

CAM_URI=$1
RTMP_OUT=$2
SCORE_THRESHOLD=$3
MODEL=$4

export CAM_URI RTMP_OUT SCORE_THRESHOLD MODEL

echo "CAM_URI=${CAM_URI}"
echo "RTMP_OUT=${RTMP_OUT}"
echo "SCORE_THRESHOLD=${SCORE_THRESHOLD}"
echo "MODEL=${MODEL}"
/opt/birdcam/venv/bin/python detect.py --cameraUri ${CAM_URI} --rtmpOut ${RTMP_OUT} --scoreThreshold ${SCORE_THRESHOLD} --model ${MODEL}
