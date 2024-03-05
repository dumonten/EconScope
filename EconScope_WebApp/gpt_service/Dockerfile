FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /gpt_service
COPY requirements.txt /gpt_service/requirements.txt
RUN pip install -r requirements.txt
RUN pip install pika==1.3.2
RUN pip install numpy
COPY . /gpt_service