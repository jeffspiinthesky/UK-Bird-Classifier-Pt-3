#!/bin/bash

CAM_URI=$1
RTMP_OUT=$2
SCORE_THRESHOLD=$3
MODEL=$4

export CAM_URI RTMP_OUT SCORE_THRESHOLD MODEL

/opt/birdcam/venv/bin/python app.py
