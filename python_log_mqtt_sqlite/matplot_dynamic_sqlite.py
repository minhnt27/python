#------------------------------------------
#--- This code to interworking with Sqlite database
#--- Author: Minhnt27
#--- Date: 6th May 2020
#--- Version: 1.0
#--- Python Ver: 3.7
#--- ref from: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#--- Sqlite install: https://freetuts.net/huong-dan-cai-dat-sqlite-1720.html
#------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
import json
import sqlite3

# SQLite DB Name
#DB_Name =  r"C:\Users\minhnt27\Downloads\sqlite\testDB.db"
DB_Name =  r"D:\lab\sqlite\testDB.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def select_db_record(self, sql_query):
        results = self.cur.execute(sql_query)
        return results

    def create_table(self, create_table_sql):
        try:
            self.cur.execute(create_table_sql)
        except Exception as e:
            print(e)

    def drop_table(self, drop_table_sql):
        try:
            self.cur.execute(drop_table_sql)
        except Exception as e:
            print(e)
            
    def __del__(self):
        self.cur.close()
        self.conn.close()

#===============================================================
# Functions to work with table SensorData

# Function to read DB Table
def Sensor_Data_Read():
    dbObj = DatabaseManager()
    results=dbObj.select_db_record("select Date_n_Time, Message from SensorData ORDER BY Date_n_Time DESC LIMIT 100;")
    rows = results.fetchall()
    #fetchall() fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch
    return rows


def animate(i):
    rows=Sensor_Data_Read()
    xs = []
    ys = []
    for row in rows:
        xs.append(float(row[0]))
        ys.append(random.randint(0,10))

    ax1.clear()
    ax1.plot(xs, ys)
    
#================================================================
#Main test 

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()