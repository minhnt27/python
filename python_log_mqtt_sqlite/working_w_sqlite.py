#------------------------------------------
#--- This code to interworking with Sqlite database
#--- Author: Minhnt27
#--- Date: 6th May 2020
#--- Version: 1.0
#--- Python Ver: 3.7
#--- ref from: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#--- Sqlite install: https://freetuts.net/huong-dan-cai-dat-sqlite-1720.html
#------------------------------------------


import json
import sqlite3

# SQLite DB Name
DB_Name =  r"C:\Users\minhnt27\Downloads\sqlite\testDB.db"

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

	def create_table(self, create_table_sql):
		try:
			self.cur.execute(create_table_sql)
		except Error as e:
			print(e)
		
	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to init Table
def New_Table():
    sql_create_table = """ CREATE TABLE IF NOT EXISTS SensorData (
                                        Id integer PRIMARY KEY NOT NULL,
                                        SensorID text,
                                        Date_n_Time text,
                                        Topic text,
                                        Message text
                                    ); """
    dbObj = DatabaseManager()
    dbObj.create_table(sql_create_table)
    del dbObj
    print ("New table SensorData was created.")

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
def Sensor_Data_Handler(jsonData):
	""" 
	use:Sensor_Data_Handler('{"SensorID":"54321", "Date":"01/20/2020", "Topic":"test/topic", "Message":"message"}')
		jsonData = '{"SensorID":"54321", "Date":"01/20/2020", "Topic":"test/topic", "Message":"message"	}';
	"""
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['SensorID']
	Date_and_Time = json_Dict['Date']
	Topic = json_Dict['Topic']
	Message = json_Dict['Message']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into SensorData (SensorID, Date_n_Time, Topic, Message) values (?,?,?,?)",[SensorID, Date_and_Time, Topic, Message])
	del dbObj
	print ("Inserted Sensor Data into Database.")

#================================================================
#Main test 	
New_Table()
jsonData = '{"SensorID":"54321", "Date":"01/20/2020", "Topic":"test/topic", "Message":"message"	}';
Sensor_Data_Handler(jsonData)