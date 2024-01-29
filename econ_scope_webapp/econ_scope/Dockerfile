FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /esapp
COPY requirements.txt /esapp/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY . /esapp

