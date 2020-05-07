#------------------------------------------
#--- This code to plot, get data from Sqlite database
#--- Author: Minhnt27
#--- Date: 7th May 2020
#--- Version: 1.0
#--- Python Ver: 3.7
#------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
import json
import sqlite3

# SQLite DB Name
DB_Name =  r"C:\Users\minhnt27\Downloads\sqlite\testDB.db"
#DB_Name =  r"D:\lab\sqlite\testDB.db"

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
        self.cur.execute(sql_query)
        results = self.cur.fetchall()
        #fetchall() fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch
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

# Function to read last 100 record from Table
def Sensor_Data_Read():	
	#select data from DB Table
	dbObj = DatabaseManager()
	rows = dbObj.select_db_record("select Date_n_Time, Message from SensorData ORDER BY Date_n_Time DESC LIMIT 100;")
	return rows

# Function to plot animate
def animate(i):
    xs = []
    ys = []
	
	#append data to array
	rows=Sensor_Data_Read()
    for row in rows:
        try:
			xs.append(float((row[0])))
			ys.append(float((row[1])))
		except Exception as e:
            pass

	#plot
    ax1.clear()
    ax1.plot(xs, ys)
    
#================================================================
#Main test 

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
