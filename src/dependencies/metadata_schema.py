#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:49:18 2023

@author: elianther

In order to install psycopg2 the following package is required:
sudo apt-get install libpq-dev

"""
# %% IMPORT PACKAGES
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from os import environ as env
# %% STATIC ENVIRONMENT
# Use this query to determine if the table exists
QUERY = """SELECT *
FROM pg_catalog.pg_tables
WHERE
    tablename = '{}'
;
"""
# %% Create video_metadata table


def create_schema(table_name):

    metadata = MetaData()
    video_metadata = Table(
        table_name, metadata,
        Column('clip_id', String(11), primary_key=True),
        Column('clip_file_extension', String(5), nullable=False),
        Column('clip_duration', Integer, nullable=False),
        Column('clip_location', String(), nullable=False),
        # We'd like to determine this timestamp from the DB server instead
        # of the application server
        Column('insert_timestamp', DateTime(
            timezone=True), server_default=func.now(), nullable=False
        )
    )
    # Return table schema
    return video_metadata, metadata


def create_table(engine, table_name):
    # Retrieve Metadata object corresponding to table schema
    _, metadata = create_schema(table_name)

    # If the table already exists, do not create it
    # if not [engine.connect().execute(text(QUERY.format(table_name)))]:
    # Create table
    try:
        metadata.create_all(engine)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    PG_URI = env['PG_URI']
    TABLE_NAME = env['TABLE_NAME']
    engine = create_engine(PG_URI, echo=True)

    create_table(engine, TABLE_NAME)
