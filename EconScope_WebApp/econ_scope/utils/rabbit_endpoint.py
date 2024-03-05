import pika
import requests
from .rabbit_point import RabbitMQPoint

class RabbitMQEndPoint(RabbitMQPoint):
    def __init__(self, ampq_url, queue, url):
        super().__init__(ampq_url=ampq_url, callback=None, queue=queue, queue_to=None)
        self.params = pika.URLParameters(ampq_url)
        self.url = url
        del self.queue_to
        del self.callback

    def _wrapper(self, ch, method, properties, message):
        requests.post(self.url, data=message)
