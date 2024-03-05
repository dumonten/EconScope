import pika

class RabbitMQPoint:
    def __init__(self, ampq_url, callback, queue, queue_to):
        self.params = pika.URLParameters(ampq_url)
        self.connection = None
        self.channel = None
        self.queue = queue
        self.queue_to = queue_to
        self.callback = callback

    def start_consuming(self):
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self._wrapper, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        if self.channel:
            self.channel.stop_consuming()
            self.channel.queue_delete(queue=self.queue)
        if self.connection:
            self.connection.close()

    def _wrapper(self, ch, method, properties, message):
        result = self.callback(message)
        properties = pika.BasicProperties(self.queue_to)
        self.channel.basic_publish(exchange="", routing_key=self.queue_to, body=result, properties=properties)
