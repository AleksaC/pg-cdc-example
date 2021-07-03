# pg-cdc-example

[![license](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Simple example testing usage of postgres [streaming replication](https://www.postgresql.org/docs/9.5/protocol-replication.html) for cdc.

## Motivation

The main reason for testing this out was to find a simple solution for syncing
a postgres database with algolia. During my initial research on the topic I
found out that [debezium](https://github.com/debezium/debezium) could be used
for this purpose, and I considered using it, but bringing in Kafka or a similar
streaming platform would be an overkill for most small/medium applications.
While it's possible to use debezium without those systems, by writing a custom
sink for debezium server or embedding debezium engine, I didn't really want to
write Java and it still seemed like there should be a simpler solution that
doesn't need a whole framework to do the job. While there are other examples of
using logical replication, they either contain stuff that's not needed for
simple examples or don't include database setup so they aren't as easy to get
started with.

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
docker-compose exec cdc python test_consumer.py
```

## Contact

- [Personal website](https://aleksac.me)
- <a target="_blank" href="http://twitter.com/aleksa_c_"><img alt='Twitter followers' src="https://img.shields.io/twitter/follow/aleksa_c_.svg?style=social"></a>
- aleksacukovic1@gmail.com
