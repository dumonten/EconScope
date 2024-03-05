from utils import RabbitMQPoint, Gpt

def receipt_data_analyze(message):
    message = Gpt.receipt_ask(message)
    return message


if __name__ == "__main__":
    ampq_url = 'amqps://oythsbqw:kADpJw3x8b7qKo_gHiirOJupaj-nI1F3@kangaroo.rmq.cloudamqp.com/oythsbqw' 
    consumer = RabbitMQPoint(ampq_url=ampq_url, callback=receipt_data_analyze, queue="gpt", queue_to="server")
    try:
        consumer.start_consuming()
    except Exception as e:
        consumer.stop_consuming()
