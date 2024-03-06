FROM python:3.10-bullseye

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

WORKDIR /opt/code
CMD /opt/code/run_service.sh
