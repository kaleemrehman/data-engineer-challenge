##### when runing this file with command line give date input as dd/mm/yy
import sqlalchemy
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from sqlalchemy.orm import sessionmaker
from isbntools.app import *
import json
from datetime import datetime


pd.set_option('display.max_colwidth', None)
SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{database}'.format(host='localhost', 
	                                                                                    port=5432, 
	                                                                                    user='postgres', 
	                                                                                    password='ovFPCzqbDN2XI0Ax', 
	                                                                                    database='nyt')
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
#if input not given or incorect will run with default value of date 22/07/2018
try:
    most_recent_date=datetime.strptime(sys.argv[1],'%d/%m/%y').date()
except:
        print("Using default Date")
        q = engine.execute('select max(published_date) as most_recent_date from bestsellers')
        res = q.fetchall()[0][0]
        most_recent_date = res.date()

table_name="bestsellers_"+most_recent_date.strftime('%Y_%m_%d')
engine.execute(f"drop table if exists {table_name}")
engine.execute(f"create table {table_name} as (select * from bestsellers WHERE 1=2)")
engine.execute(f"insert into {table_name} select * from bestsellers where published_date = '{most_recent_date}'")



engine.execute(f"delete from bestsellers where published_date = '{most_recent_date}'")

missing_info_records=pd.read_sql(f"select * from {table_name} where title is NULL or author is NULL", engine)


for index, row in missing_info_records.iterrows():
    
    try:
        book_info=registry.bibformatters['json'](meta(row['isbn']))
        book_info_json=json.loads(book_info)
        query = f"update {table_name} set title = '{book_info_json['title']}', author='{book_info_json['author'][0]['name']}' where isbn='{row['isbn']}'"
        engine.execute(query)
    except:
        print(f"Author or title name is missing for ISBN {row['isbn']} in isbntools")

        
