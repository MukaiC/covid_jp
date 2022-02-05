import mysql.connector
import pandas as pd

'''
Retrieve data from the covid database and save it as a csv file
'''

# connect to database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
)

# retrieve all from table cases_airport_jp
sql = ''' SELECT * FROM covid.cases_airport_jp'''

df = pd.read_sql_query(sql=sql, con=mydb)

# save it as csv
df.to_csv('cases_airport_jp.csv', index=False)


