import pika, json

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish():
    # properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='test', body='make hello')
