import json
import time
from pprint import pprint

import psycopg2
import psycopg2.extras


class DemoConsumer:
    def __call__(self, msg):
        data = json.loads(msg.payload)
        # TODO: add actual algolia push example
        pprint(data)
        msg.cursor.send_feedback(flush_lsn=msg.data_start)


TIMEOUT = 10


def main():
    t = 0

    while t < TIMEOUT:
        try:
            # TODO: allow passing args or setting connection params through env variable
            conn = psycopg2.connect(
                "host=localhost dbname=test user=replication_role password=test",
                connection_factory=psycopg2.extras.LogicalReplicationConnection,
            )
            break
        except psycopg2.OperationalError:
            pass

        t += 1
        time.sleep(1)
    else:
        print("Couldn't connect to database in 10s")
        return 1

    cur = conn.cursor()
    try:
        cur.start_replication(slot_name="pytest", decode=True)
    except psycopg2.ProgrammingError:
        cur.create_replication_slot("pytest", output_plugin="wal2json")
        cur.start_replication(slot_name="pytest", decode=True)

    democonsumer = DemoConsumer()

    print("Starting streaming, press Control-C to end...")

    try:
        cur.consume_stream(democonsumer)
    except KeyboardInterrupt:
        cur.close()
        conn.close()

        print(
            "The slot 'pytest' still exists. Drop it with "
            "SELECT pg_drop_replication_slot('pytest'); if no longer needed."
        )
        print(
            "WARNING: Transaction logs will accumulate in pg_xlog "
            "until the slot is dropped."
        )

        return 0


if __name__ == "__main__":
    exit(main())
