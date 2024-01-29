import pika

from gpt import ask

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='gpt')


def callback(ch, method, properties, body):
    if method == "gpt":
        response = ask(body)
        properties = pika.BasicProperties("gpt_answer")
        channel.basic_publish(exchange='', routing_key='test', body=response, properties=properties)


channel.basic_consume(queue='gpt', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
