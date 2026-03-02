import json
from lasair import lasair_consumer

kafka_server = 'lasair-lsst-kafka.lsst.ac.uk:9092'
my_topic     = 'lasair_1Lightweight'

group_id     = 'test12'
consumer = lasair_consumer(kafka_server, group_id, my_topic)
import json
n = 0
while n < 10:
    msg = consumer.poll(timeout=20)
    if msg is None:
        break
    if msg.error():
        print(str(msg.error()))
        break
    result = json.loads(msg.value())
    print(json.dumps(result, indent=2))
    n += 1
print(n, 'messages')

