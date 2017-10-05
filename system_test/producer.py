# -*- coding: utf-8 -*-
import json
import os
import logging

import kafka
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)
logger = logging.getLogger(__name__)


KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC = os.getenv('KAFKA_TOPIC', 'my_topic')


def get_producer():
    for _ in range(20):
        try:
            producer = KafkaProducer(
                    bootstrap_servers=KAFKA_SERVER,
                    value_serializer=lambda data: json.dumps(data).encode())
        except kafka.errors.KafkaError:
            time.sleep(1)
        else:
            return producer


producer = get_producer()


def produce(topic, data):
    future = producer.send(topic, data)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as err:
        logger.error(err)
    else:
        logger.debug("record_metadata: %s", record_metadata)


if __name__ == '__main__':
    produce(TOPIC, {'test': 'ok'})
