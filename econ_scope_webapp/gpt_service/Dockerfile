FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /gpt-service
COPY requirements.txt /gpt-service/requirements.txt
RUN pip install -r requirements.txt
COPY . /gpt-service

