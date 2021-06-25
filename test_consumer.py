#!/usr/bin/env python
import psycopg2

from stream_consumer import get_db_connection_params


def main():
    conn = psycopg2.connect(**get_db_connection_params())
    cur = conn.cursor()

    cur.execute("INSERT INTO test (name) VALUES (%s)", ("john",))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    exit(main())
