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
import time

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
def updatefig(i):
    xs = []
    ys = []
	
	#append data to array
    rows=Sensor_Data_Read()
    for row in rows:
        try:
			#The strip() method returns a copy of the string by removing both the leading and the trailing characters string.strip([chars])
            #check string empty. Empty strings are "falsy" which means they are considered false in a Boolean context. ref:https://www.tutorialspoint.com
            if(row[0].strip() and row[1].strip()):
                x=float(row[0])
                y=float(row[1])
                xs.append(x)
                ys.append(y)
        except Exception as e:
            pass

    #plot
    ax1.clear()
    ax1.plot(xs, ys)
    
#================================================================
#Main test 
#The time() function returns the number of seconds passed since epoch
start_time = time.time()
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
try:
    ani = animation.FuncAnimation(fig, updatefig, interval=100)
    plt.show()
except:
    pass
finally:
    end_time = time.time() 
    print("run time: "+ str(round((end_time-start_time)/(24*60*60),2))+" days")
	
	
"""
The try block lets you test a block of code for errors.
The except block lets you handle the error.
The finally block lets you execute code, regardless of the result of the try- and except blocks.

The pass statement in Python is used when a statement is required syntactically but you do not want any command or code to execute.
The pass statement is a null operation; nothing happens when it executes
The break statement in Python terminates the current loop and resumes execution at the next statement
The continue statement in Python returns the control to the beginning of the while loop. The continue statement rejects all the remaining statements in the current iteration of the loop and moves the control back to the top of the loop.

"""