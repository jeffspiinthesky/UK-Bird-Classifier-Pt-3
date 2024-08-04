# UK Bird Classification Part 3

## Introduction
Part 3 of this project takes us forward from identifying birds in a static photograph and, instead, uses our custom data model to identify birds in realtime on a video feed from an IP webcam

## Build
* Encsure docker and docker-compose are installed:
```
apt update && apt install -y docker docker.io docker-compose
```
* Clone this repo and move into the directory created, then:
```
docker build -t birdcam_au:0.0.1 -f Dockerfile .
```

## Run
You'll need to edit the following environment variables in the file birdcam-ai.yml:
* CAM_URI - Set this to the URI of your IP camera e.g. ```rtsp://user:password@192.168.0.20/camera```
* RTMP_OUT - Set this to the RTMP endpoint of your NGINX container running rtmp_nginx_module e.g. ```rtmp://192.168.0.21/birdcam_live```

Also, you'll need to edit the location of your bird AI data model in the volumes section to point to your bird model e.g.
* ```- /mnt/src/UK-Bird-Classifier-Pt-2/bird_model.tflite:/opt/birdcam/model/bird_model.tflite```
Then you can run the application with
```
docker-compose -f birdcam-ai.yml up -d
```
You can check that this is working by opening a video player such as VLC, opening a network path and entering the value of your RTMP_OUT as the URI to open.

You should then see your video stream and, as birds hit your feeder, they'll get identified by your data model in realtime!!