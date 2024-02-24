# django-kafka-demo

Creating a Django application that demonstrates how to consume messages from and produce messages to a Kafka broker 
involves integrating Kafka into a Django project.


Key Components of the Integration
Kafka Producer and Consumer: 
The Django app will include functionality to produce messages to a Kafka topic and consume messages from a Kafka topic. 

Batch Processing with min_batch_size and max_batch_size: 
The consumer can be configured to process messages in batches, improving efficiency and throughput. 
By specifying min_batch_size and max_batch_size, you control the minimum and maximum number of messages to be processed in a single batch. 

min_batch_size: The minimum number of messages that triggers processing. 
max_batch_size: The maximum number of messages to process in one batch. 
Stamp Model: 
The app includes a Django model named Stamp 
with fields such as time_tolerance and created_date. 
These fields allow the application to handle messages based on temporal logic.

time_tolerance: This field can be used to determine how long to wait before processing a message.
created_date: The timestamp when the message was created or sent to Kafka. 

MessageBatchProcessor Logic: 
This component encapsulates the logic for batch processing of messages. 
It checks each message to determine if it's ready for processing, 
either because the batch has reached min_batch_size or 
because the message meets the criteria based on created_date and time_tolerance.

Processing Scenarios
Batch Size Exceeded:
When the number of accumulated messages exceeds min_batch_size, 
the MessageBatchProcessor triggers processing of the batch. 
This scenario optimizes for throughput by ensuring that messages are processed in substantial batches.

Time-Based Processing: 
In addition to batch size, messages can be processed based on their created_date and time_tolerance. 
If a message's processing time has come according to these fields, it can be processed even if the min_batch_size has not been reached. 
This ensures that messages are not unnecessarily delayed, balancing timely processing with batch efficiency.


### Install

Setup kafka
```
 https://downloads.apache.org/kafka/3.5.1/kafka_2.12-3.5.1.tgz
 tar -xzf kafka_2.12-3.5.1.tgz
 cd kafka_2.12-3.5.1
 run in terminal 
 KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
 bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

 run in terminal #1
 bin/kafka-server-start.sh config/kraft/server.properties
 run in terminal #2
 bin/kafka-console-consumer.sh  --topic topic_data_created  --bootstrap-server localhost:9092 --from-beginning
```

Create and source a virtual environment:
```
eval "$(pyenv init -)"
Python 3.9.17

python3 -m venv venv
source venv/bin/activate
cd StampService
pip install -r requirements.txt
```

Run project
```
terminal #1
cd StampService
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```
```
terminal #2
cd StampService
python3 manage.py launch_queue_listener
```

Run tests

```
cd StampService
python3 manage.py test
```

Test with payload, default batchsize set to 2 in queue_listener.py

```
curl --request POST \
  --url http://127.0.0.1:8000/datasender/create_stamp/ \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data object_cid=1 \
  --data time_tolerance=10
  
 curl --request POST \
  --url http://127.0.0.1:8000/datasender/create_stamp/ \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data object_cid=2 \
  --data time_tolerance=10
  
```