import pika
from rest_framework.response import Response

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='test')


def callback(ch, method, properties, body):
    print('Received')
    print(body)

channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
