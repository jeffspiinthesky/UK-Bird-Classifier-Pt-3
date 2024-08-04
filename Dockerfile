FROM ubuntu:22.04

RUN apt update 
RUN apt upgrade -y

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt install -y python3 python3-pip curl git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev x264 ffmpeg

RUN mkdir /opt/birdcam
WORKDIR /opt/birdcam

RUN curl https://pyenv.run | bash
ENV HOME=/root
ENV PYENV_ROOT="${HOME}/.pyenv" 
ENV PATH="${PYENV_ROOT}/bin:${PATH}"
RUN pyenv init --path
RUN pyenv init -
ADD bashrc_addition /tmp/bashrc_addition
RUN cat /tmp/bashrc_addition >> /root/.bashrc
RUN pyenv install 3.12.4
RUN pyenv global 3.12.4
RUN /root/.pyenv/shims/python -m venv venv

RUN /opt/birdcam/venv/bin/pip install --upgrade pip
RUN /opt/birdcam/venv/bin/pip install argparse opencv-python mediapipe

ADD detect.py /opt/birdcam/detect.py
ADD utils.py /opt/birdcam/utils.py
ADD docker-entrypoint.sh /opt/birdcam/docker-entrypoint.sh

VOLUME /opt/birdcam/model

ENV CAM_URI='http://1.2.3.4/cam'
ENV RTMP_OUT="rtmp://1.2.3.4/birdcam_live"
ENV SCORE_THRESHOLD=0.40
ENV MODEL=/opt/birdcam/model/bird_model.tflite

ENTRYPOINT [ "/bin/bash", "-c", "/opt/birdcam/docker-entrypoint.sh ${CAM_URI} ${RTMP_OUT} ${SCORE_THRESHOLD} ${MODEL}" ]