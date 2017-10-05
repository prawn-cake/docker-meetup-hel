# -*- coding: utf-8 -*-
from kafka import KafkaProducer
import logging

from kafka.errors import KafkaError

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)

if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    future = producer.send('my_topic', b'test-msg')

    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as err:
        # Decide what to do if produce request failed...
        logging.error(err)
        pass
