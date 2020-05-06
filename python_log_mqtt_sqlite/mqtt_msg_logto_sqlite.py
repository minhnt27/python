#------------------------------------------
#--- This code create a client, which subcribe a topic "test/topic" on server "test.mosquitto.org"
#--- and loop forever waiting a mesage comming to print out
#--- Author: Minhnt27
#--- Date: 6th May 2020
#--- Version: 1.0
#--- Python Ver: 3.7
#--- ref from: https://pypi.org/project/paho-mqtt/
#--- lib installation cmd: pip install paho-mqtt
#------------------------------------------

import json
import sqlite3
import paho.mqtt.client as mqtt

# SQLite DB Name
#DB_Name =  r"C:\Users\minhnt27\Downloads\sqlite\testDB.db"
DB_Name =  r"D:\lab\sqlite\testDB.db"
topic="test/topic"
server="192.168.1.6"
keepalive=60
port=1883

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
# Functions to interwork with SQLite

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


# Function to save Sensor data to DB Table
def Sensor_Data_Loger(jsonData):
    """ use:Sensor_Data_Handler('{"SensorID":"54321", "Date":"01/20/2020", "Topic":"test/topic", "Message":"message"}')
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


#==============================================================
# Funtions to interwork with mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(dir(msg));
    #for debug object message
    print(str(msg.timestamp)+" "+msg.topic+" "+str(msg.payload))
    #Log to database - send a json format
    dataset01 = {"SensorID":"12345", "Date":msg.timestamp, "Topic":msg.topic, "Message":str(msg.payload)}
    json_dump = json.dumps(dataset01)
    Sensor_Data_Loger(json_dump)
    
#===============================================================

New_Table()

# Main mqtt client works
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, port, keepalive)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()