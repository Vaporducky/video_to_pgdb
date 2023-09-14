#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:14:43 2023

@author: elianther
"""

# %% IMPORT PACKAGES
import argparse
import logging
from os import environ as env
from sqlalchemy import create_engine

from dependencies.downloader import download_video
from dependencies.add_record import add_db_record, add_csv_record
from dependencies.metadata_schema import create_schema
from dependencies.splitter import video_splitter
# %% MAIN


def pipeline(engine, url, ingestion_path, process_path, table_name):
    logging.info('START - Pipeline')
    # Download video
    logging.info(f'Download video: {url}')
    data_dict, output_file = download_video(url, ingestion_path)
    # If successful, add record to DB and create CSV file
    TABLE_SCHEMA, _ = create_schema(table_name)
    logging.info(f'Adding records to the DB')
    add_db_record(engine, data_dict, TABLE_SCHEMA)
    logging.info(f'Adding records to the CSV report')
    add_csv_record(data_dict, process_path)
    # Split video
    video_splitter(output_file, process_path)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    # Define static environment
    parser = argparse.ArgumentParser()
    parse_url = parser.add_mutually_exclusive_group()
    parse_url.add_argument('--url',
                           dest='URL',
                           nargs='*',
                           action='store',
                           type=str,
                           help='A valid YouTube URL. e.g. https://www.youtube.com/watch?v=4fezP875xOQ')
    parse_url.add_argument('--url-file',
                           dest='URL_FILE',
                           type=str,
                           help='A new line file containing valid YouTube URLs per line.')

    args = parser.parse_args()
    # Environment variables
    PG_URI = env['PG_URI']
    TABLE_NAME = env['TABLE_NAME']
    INGESTION_PATH = env['INGESTION_PATH']
    PROCESS_PATH = env['PROCESS_PATH']
    # Establish connection to the DB
    engine = create_engine(PG_URI, echo=True)
    if args.URL_FILE is None:
        print(args.URL)
# =============================================================================
#         for url in args.URL:
#             pipeline(engine, url, INGESTION_PATH, PROCESS_PATH, TABLE_NAME)
# =============================================================================
    elif args.URL is None:
        for url in open(args.URL_FILE, 'r').readlines():
            pipeline(engine, url, INGESTION_PATH, PROCESS_PATH, TABLE_NAME)
