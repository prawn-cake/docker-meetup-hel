# -*- coding: utf-8 -*-
import json
import logging
import os
import time
import psycopg2
import psycopg2.extras as pg_extras
import psycopg2.extensions as pg_extensions
import kafka
import kafka.errors


# Register jsonb extras to convert jsonb data to dict transparently
pg_extras.register_default_jsonb(globally=True)
pg_extensions.register_adapter(dict, psycopg2.extras.Json)

DB_DSN = os.getenv('DB_DSN', 'postgresql://worker:worker@localhost/meetup')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC = os.getenv('KAFKA_TOPIC', 'my_topic')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)
logger = logging.getLogger(__name__)


def get_consumer():
    """Factory method to get KafkaConsumer instance with retries logic

    :return: KafkaConsumer instance
    """
    for _ in range(20):
        try:
            consumer = kafka.KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_SERVER,
                group_id="my-group",
                value_deserializer=lambda m: json.loads(m.decode())
            )
        except kafka.errors.KafkaError as err:
            logger.warning(err)
            logger.info('Sleep 1 sec and reconnect')
            time.sleep(1)
        else:
            return consumer


def run_app():
    """Main app loop
    - get consumer
    - get messages
    - save it to a data store

    """
    consumer = get_consumer()
    for msg in consumer:
        logging.info("---> consumed: %s", msg)
        save_to_db(msg.value)


def save_to_db(data):
    with psycopg2.connect(dsn=DB_DSN) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO events(data) VALUES(%s)", (data, ))

    logger.info('save_to_db: %s', data)


if __name__ == '__main__':
    run_app()
