import json
from confluent_kafka import Producer
import socket
from .kafka_config import KAFKA_DATA_CREATED_TOPIC


class ProducerDataSent:
    def __init__(self) -> None:
        # TODO extract to config
        conf = {'bootstrap.servers': "localhost:9092", 'client.id': socket.gethostname()}
        self.producer = Producer(conf)

    # This method will be called inside view for sending Kafka message
    def publish(self, method, body):
        print('Inside ProducerDataSent: Sending to Kafka: ')
        print(body)
        self.producer.produce(KAFKA_DATA_CREATED_TOPIC, key="key.data.created", value=json.dumps(body))
