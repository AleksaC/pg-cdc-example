# pg-cdc-test

[![license](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Simple example testing usage of postgres [streaming replication](https://www.postgresql.org/docs/9.5/protocol-replication.html) for cdc.

## Motivation

I used dynamodb as a primary database on one of my previous projects. Since
dynamo is really rigid when it comes to searching and filtering I used algolia
for that purpose, and I loved it. Syncing algolia with dynamo was really easy
with dynamo streams and lambdas.

Beside offering great performance and search quality algolia is basically free
for smaller projects and I want to keep using it for such projects, even for
projects that use postgres as a main database. Despite having full-text search
capabilities I found that search quality in postgres is much worse than algolia.

The only problem with using postgres with algolia is that keeping those two in
sync isn't as straightforward as with dynamodb. During my initial research on
the topic I found out that [debezium](https://github.com/debezium/debezium)
could be used for this purpose, and I considered using it, but it seemed a bit
too complicated as bringing in Kafka or a similar streaming platform was an
overkill. While it's possible to use debezium without those systems, by writing
a custom sink for debezium server or embedding debezium engine I didn't really
want to write Java and it still seemed like there should be a simpler solution
that doesn't even need a whole framework to do the job.

Later I learned that streaming replication could be used for this, but was
having a hard time finding concrete examples that were quick to test and easy
to understand. Finally, I found out that psycopg actually supports postgres
replication protocol and found an example that does this and was able to quickly
expand on it and do what needed.

## About

The example uses [`wal2json`](https://github.com/eulerto/wal2json) output plugin
for [logical decoding](https://www.postgresql.org/docs/9.4/logicaldecoding-explanation.html).
If you are not using the provided docker image for the database, you are going
to have to install the plugin yourself. You can also use other plugins, or use
built in `test_decoding` plugin.

The example just prints the decoded json from the message payload. It takes
messages in batches, either waiting for a batch to fill up or a batch timeout
to pass before consuming it.

## Getting started

The following commands will set up docker containers with a test database and
a replication stream consumer and perform an insert into the test database:

```shell
docker-compose up
./test_consumer.py
```

## Contact

- [Personal website](https://aleksac.me)
- <a target="_blank" href="http://twitter.com/aleksa_c_"><img alt='Twitter followers' src="https://img.shields.io/twitter/follow/aleksa_c_.svg?style=social"></a>
- aleksacukovic1@gmail.com
