#!/usr/bin/env python

import contextlib
import json
import os
import time
from datetime import datetime
from pprint import pprint
from select import select

import psycopg2
import psycopg2.extras


def consume_batch(msgs):
    cursor = msgs[0].cursor

    for msg in msgs:
        assert cursor == msg.cursor

    for msg in msgs:
        data = json.loads(msg.payload)
        pprint(data)

    cursor.send_feedback(
        flush_lsn=max(map(lambda msg: msg.data_start, msgs)), force=True
    )


def consume_stream(cur, consumer, **options):
    status_interval = options.get("status_interval", 10.0)
    batch_timeout = options.get("batch_timeout", 1.0)
    batch_size = options.get("batch_size", 10)

    msg_batch = []
    first_msg_ts = None

    while True:
        if not msg_batch:
            first_msg_ts = None

        if msg := cur.read_message():
            msg_batch.append(msg)

            if not first_msg_ts:
                first_msg_ts = datetime.now()

            if len(msg_batch) == batch_size:
                consumer(msg_batch)
                msg_batch = []
        else:
            now = datetime.now()
            timeout = (
                status_interval - (now - cur.feedback_timestamp).total_seconds()
                if not first_msg_ts
                else batch_timeout - (now - first_msg_ts).total_seconds()
            )

            with contextlib.suppress(InterruptedError):
                select([cur], [], [], max(0, timeout))

            if first_msg_ts and (now - first_msg_ts).total_seconds() >= batch_timeout:
                consumer(msg_batch)
                msg_batch = []


def get_db_connection_params():
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", 5432)),
        "dbname": os.environ.get("DB_NAME", "test"),
        "user": os.environ.get("DB_USER", "replication_role"),
        "password": os.environ.get("DB_PASSWORD", "test"),
    }


TIMEOUT = 10
MAX_RETRIES = 10


def main():
    retries = 0

    while retries < MAX_RETRIES:
        with contextlib.suppress(psycopg2.OperationalError):
            conn = psycopg2.connect(
                **get_db_connection_params(),
                connection_factory=psycopg2.extras.LogicalReplicationConnection,
            )
            break
        retries += 1
        time.sleep(TIMEOUT / MAX_RETRIES)
    else:
        print(f"Couldn't connect to database in {TIMEOUT}s")
        return 1

    cur = conn.cursor()

    try:
        cur.start_replication(slot_name="test", decode=True)
    except psycopg2.ProgrammingError:
        cur.create_replication_slot("test", output_plugin="wal2json")
        cur.start_replication(slot_name="test", decode=True)

    print("Starting streaming, press Control-C to end...")

    try:
        consume_stream(cur, consume_batch)
    except KeyboardInterrupt:
        cur.close()
        conn.close()

        print(
            "WARNING: The slot 'test' still exists. Transaction logs will accumulate "
            "in pg_xlog until the slot is dropped. Drop it with "
            "`SELECT pg_drop_replication_slot('test');` if no longer needed."
        )

        return 0


if __name__ == "__main__":
    exit(main())
