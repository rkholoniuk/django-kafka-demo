import json
import threading
import time
from datetime import datetime
from datetime import timezone
from dateutil import parser
from confluent_kafka import Consumer, KafkaError, KafkaException
from .batch_processor import MessageBatchProcessor, Message
from .kafka_config import KAFKA_CONFIG, KAFKA_DATA_CREATED_TOPIC

running = True
batch_size = 2


class DataCreatedListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.consumer = Consumer(KAFKA_CONFIG)
        self.processor = MessageBatchProcessor(min_batch_size=batch_size)

    def run(self):
        self.consumer.subscribe([KAFKA_DATA_CREATED_TOPIC])
        try:
            while running:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    self.processor.check_and_process_messages()
                    time.sleep(1)
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:  # Ignore EOF
                        print(f"Kafka error: {msg.error()}")
                    continue

                try:
                    message_data_str = msg.value().decode('utf-8')
                    message_data = json.loads(message_data_str)

                    # Check if the result is still a string, which might indicate double-encoding
                    if isinstance(message_data, str):
                        message_data = json.loads(message_data)

                    if not isinstance(message_data, dict):
                        print(f"Expected dict, got {type(message_data)}: {message_data}")
                        continue  # Skip this message

                    created_date = parser.parse(message_data['created_date'])
                    message = Message(
                        object_cid=message_data['object_cid'],
                        time_tolerance=message_data['time_tolerance'],
                        created_date=created_date
                    )
                    print(f"Message {type(message)}: {message}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue
                except KeyError as e:
                    print(f"Missing key in message data: {e}")
                    continue
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error creating message: {e}")
                    continue

                # Successfully created message, now process it
                self.processor.append_message(message)

        except KafkaException as e:
            print(f"Kafka exception: {e}")
        finally:
            self.consumer.close()
