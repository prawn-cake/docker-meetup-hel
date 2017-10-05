# -*- coding: utf-8 -*-
from aiokafka import AIOKafkaConsumer
import asyncio

from kafka import KafkaConsumer
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)
loop = asyncio.get_event_loop()


async def consume():
    # FIXME: it fails here
    # https://github.com/aio-libs/aiokafka/blob/master/aiokafka/client.py#L446
    consumer = AIOKafkaConsumer(
        'my_topic1',
        loop=loop, bootstrap_servers=['localhost:9092'],
        group_id="my-group")

    # Get cluster layout and join group `my-group`
    await consumer.start()

    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


def consume_sync():
    consumer = KafkaConsumer(
        'my_topic',
        bootstrap_servers=['localhost:9092'],
        group_id="my-group")
    for msg in consumer:
        print("consumed: ", msg.topic, msg.partition, msg.offset,
              msg.key, msg.value, msg.timestamp)


if __name__ == '__main__':
    # loop.run_until_complete(consume())
    consume_sync()
