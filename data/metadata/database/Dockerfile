FROM postgres:15.4-alpine3.18

LABEL author="Aesthetic Datum"
LABEL description="A mock DB to test an ingestion pipeline. This DB is used as a metadata store."
LABEL version="1.0"

COPY db_init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
