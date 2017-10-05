# -*- coding: utf-8 -*-
import os
import os.path as op
import json
from json import JSONDecodeError

import psycopg2
import pytest
import time
from producer import produce


DB_DSN = os.getenv('DB_DSN', 'postgresql://worker:worker@localhost/meetup')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC = 'my_topic'


@pytest.fixture
def wiki_updates():
    """Read wiki updates fixture

    """
    updates = []
    cur_dir = op.abspath(op.dirname(__file__))
    with open(op.join(cur_dir, 'wiki_updates.txt')) as fd:
        for line in fd.readlines():
            try:
                updates.append(json.loads(line.strip()))
            except JSONDecodeError:
                pass
    return updates


@pytest.fixture
def db_conn():
    for _ in range(20):
        try:
            conn = psycopg2.connect(dsn=DB_DSN)
        except psycopg2.OperationalError:
            print('DB connection error. Retry in 1 sec')
            time.sleep(1)
        else:
            return conn


def setup_module(module):
    print('Run setup_module')
    # time.sleep(20)
    print('Sleep 20')
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM events")


def test_state(db_conn, wiki_updates):
    # Publish events to the event bus
    for update in wiki_updates:
        produce(TOPIC, update)

    # Wait for processing
    time.sleep(10)

    with db_conn as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT data -> 'meta' ->> 'domain' AS domain, COUNT(*) AS cnt "
            "FROM events "
            "GROUP BY domain "
            "ORDER BY cnt DESC;"
        )
        res = dict(cur.fetchall())

    assert res['www.wikidata.org'] == 34
    assert res['en.wikipedia.org'] == 10
    assert res['commons.wikimedia.org'] == 10
