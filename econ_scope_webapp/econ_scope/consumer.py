import pika
from rest_framework.response import Response

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received')
    print(body)
    # res = '<h1>'+ str(body) + '</h1>'
    return Response('<h1> FIOOOOOL  </h1>')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()