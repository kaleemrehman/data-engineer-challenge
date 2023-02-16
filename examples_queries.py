import sqlalchemy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', -1)

if __name__ == '__main__':
	SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{database}'.format(host='localhost', 
	                                                                                    port=5432, 
	                                                                                    user='postgres', 
	                                                                                    password='ovFPCzqbDN2XI0Ax', 
	                                                                                    database='nyt')
	engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

	random_sample = pd.read_sql("select * from bestsellers order by random() limit 5", engine)
	print('random sample', random_sample)

	q = engine.execute('select max(published_date) as most_recent_date from bestsellers')
	res = q.fetchall()[0][0]
 
	most_recent_date = res.date()
	print(most_recent_date)

	most_recent_bestsellers = pd.read_sql(f"select * from bestsellers where published_date = '{most_recent_date}'", engine)
	print(most_recent_bestsellers)