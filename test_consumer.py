#!/usr/bin/env python
import psycopg2


def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="test",
        user="replication_role",
        password="test",
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO test (name) VALUES (%s)", ("john",))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    exit(main())
