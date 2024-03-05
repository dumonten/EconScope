import pika
from utils import ImageConverter

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(body):
    encoded_message = ImageConverter.encode(body)
    properties = pika.BasicProperties("seg")
    channel.basic_publish(exchange='', routing_key='seg', body=encoded_message, properties=properties)
    