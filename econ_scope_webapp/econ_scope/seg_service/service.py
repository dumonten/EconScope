import pika
import numpy as np
import cv2

from segmentation import crop_image, im2json, json2im

params = pika.URLParameters('amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='seg')


def callback(ch, method, properties, body):
    if properties.content_type == "segmentation":
        print("here")
        message = json2im(body)
        np_array = cv2.imdecode(np.frombuffer(message["image"], np.uint8), cv2.IMREAD_COLOR)
        cropped_image = crop_image(np_array)
        message["image"] = cv2.imencode(".jpg", cropped_image)[1].tobytes()
        message = im2json(message)
        properties = pika.BasicProperties("segmentation_answer")
        channel.basic_publish(exchange='', routing_key='rec', body=message, properties=properties)


channel.basic_consume(queue='seg', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
