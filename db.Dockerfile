FROM postgres:13-buster

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        postgresql-13-wal2json \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :
