import pika
import numpy as np
import cv2

from image_converter import ImageConverter
from receipt_detector import ReceiptDetector

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='seg')


def callback(ch, method, properties, message):
    if properties.content_type == "segmentation":
        message = ImageConverter.decode(message)
        np_array = cv2.imdecode(np.frombuffer(message["image"], np.uint8), cv2.IMREAD_COLOR)
        np_array = cv2.cvtColor(np_array, cv2.COLOR_BGR2RGB)
        receipt = ReceiptDetector.detect(np_array)
        message["image"] = cv2.imencode(".jpg", receipt)[1].tobytes()
        message = ImageConverter.encode(message)
        properties = pika.BasicProperties("segmentation_answer")
        channel.basic_publish(exchange='', routing_key='rec', body=message, properties=properties)


channel.basic_consume(queue='seg', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
