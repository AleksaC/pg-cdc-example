CREATE DATABASE test;

CREATE ROLE
    replication_role
WITH
    REPLICATION
    LOGIN
    PASSWORD 'test';

\c test;

SET SESSION ROLE replication_role;

CREATE TABLE test (
    id SERIAL PRIMARY KEY,
    name TEXT
);
