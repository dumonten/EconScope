FROM python:3.10.12
ENV PYTHONUNBUFFERED 1
WORKDIR /seg_service
RUN git clone https://github.com/open-mmlab/mmdetection.git
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install -U openmim
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install scikit-image
RUN mim install mmengine
RUN mim install 'mmcv>=2.0.0'
RUN mim install mmdet
RUN pip install pika==1.3.2
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
RUN pip install pytesseract
RUN pip install opencv-contrib-python
RUN pip install imutils
COPY . /seg_service