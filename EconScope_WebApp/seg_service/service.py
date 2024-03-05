import numpy as np
import cv2

from utils import RabbitMQPoint, ReceiptDetector, ImageConverter


def receipt_detect(message):
    message = ImageConverter.decode(message)
    np_array = cv2.imdecode(np.frombuffer(message["image"], np.uint8), cv2.IMREAD_COLOR)
    np_array = cv2.cvtColor(np_array, cv2.COLOR_BGR2RGB)
    receipt = ReceiptDetector.detect(np_array)
    message["image"] = cv2.imencode(".jpg", receipt)[1].tobytes()
    message = ImageConverter.encode(message)
    return message


if __name__ == "__main__":
    ampq_url = 'amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw' 
    consumer = RabbitMQPoint(ampq_url=ampq_url, callback=receipt_detect, queue="seg", queue_to="rec")
    try:
        consumer.start_consuming()
    except Exception as e:
        consumer.stop_consuming()

while True: pass