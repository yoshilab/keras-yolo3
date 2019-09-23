FROM tensorflow/tensorflow:latest-gpu-py3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y python-opencv \
    && pip install --upgrade opencv-python keras tqdm \
    && pip install keras-segmentation

RUN apt install -y git

RUN pip install cython
RUN pip install git+https://github.com/waleedka/coco.git#subdirectory=PythonAPI

RUN apt install -y sshfs

RUN pip install matplotlib

RUN pip install pillow

WORKDIR /work