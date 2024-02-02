import pika
from convert import json2im
import requests

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='rec')


def callback(ch, method, properties, body):
    if properties.content_type == "segmentation_answer":
        print("here")
        message = json2im(body)
        url = "http://localhost:8000/internal"
        requests.post(url, data=message)
        



channel.basic_consume(queue='rec', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

channel.close()
