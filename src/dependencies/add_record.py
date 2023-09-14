#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:19:46 2023

@author: elianther
"""
# %% IMPORT PACKAGES
from pathlib import Path
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
# %%
# %% MAIN LOGIC


def add_db_record(engine, data_dict, table_schema):
    insert_statement = insert(table_schema).values(
        [data_dict])
    with engine.connect() as con:
        try:
            con.execute(insert_statement)
            con.commit()
        except IntegrityError as e:
            print(e)


def add_csv_record(data_dict, output_path):
    date = datetime.now().strftime('%Y%m%d')
    report_folder = Path(output_path).joinpath(date).joinpath('report')
    report_folder.mkdir(parents=True, exist_ok=True)

    filename = report_folder.joinpath('report' + '_' + date + '.csv')
    if not filename.is_file():
        with open(str(filename), 'w', encoding='utf-8') as f:
            # Construct string
            columns = ','.join(key for key in data_dict.keys())
            data = ','.join(str(data_dict[key]) for key in data_dict.keys())
            # Write data
            print(columns, file=f)
            print(data, file=f)
    else:
        with open(str(filename), 'a', encoding='utf-8') as f:
            # Construct string
            data = ','.join(str(data_dict[key]) for key in data_dict.keys())
            # Write data
            print(data, file=f)
