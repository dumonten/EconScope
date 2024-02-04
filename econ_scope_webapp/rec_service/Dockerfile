FROM python:3.10.12
ENV PYTHONUNBUFFERED 1
WORKDIR /rec_service
COPY requirements.txt /rec_service/requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install lmdb
RUN pip install dual
RUN pip install tight
RUN pip install data
RUN pip install prox
RUN pip install common
RUN pip install PyMuPDF
RUN pip install paddle
RUN pip install paddleocr
RUN pip install -r requirements.txt
RUN pip install pika==1.3.2
COPY . /rec_service