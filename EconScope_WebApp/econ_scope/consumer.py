import requests
from utils import RabbitMQEndPoint

if __name__ == "__main__":
    ampq_url = 'amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw' 
    consumer = RabbitMQEndPoint(ampq_url=ampq_url, queue="server", url="http://localhost:8000/internal")
    try:
        consumer.start_consuming()
    except Exception as e:
        consumer.stop_consuming()
