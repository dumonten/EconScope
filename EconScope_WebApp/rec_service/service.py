import numpy as np
import cv2
from utils import TextRecognizer, ImageConverter, RabbitMQPoint

def receipt_data_analyze(message):
    message = ImageConverter.decode(message)
    np_array = cv2.imdecode(np.frombuffer(message["image"], np.uint8), cv2.IMREAD_COLOR)
    text = TextRecognizer.get_text(np_array)
    return text


if __name__ == "__main__":
    ampq_url = 'amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw' 
    consumer = RabbitMQPoint(ampq_url=ampq_url, callback=receipt_data_analyze, queue="rec", queue_to="gpt")
    try:
        consumer.start_consuming()
    except Exception as e:
        consumer.stop_consuming()
