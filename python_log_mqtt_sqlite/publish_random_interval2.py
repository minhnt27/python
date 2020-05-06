#------------------------------------------
#--- This code create a client, which publish (with interval 2s) a random 0-10
#--- Author: Minhnt27
#--- Date: 6th May 2020
#--- Version: 1.0
#--- Python Ver: 3.7
#--- ref from: https://pypi.org/project/paho-mqtt/
#--- lib installation cmd: pip install paho-mqtt
#------------------------------------------

import paho.mqtt.client as mqtt
import random
import time

#================================================
# test with topic "test/topic" on server "test.mosquitto.org"
topic="test/topic"
server="test.mosquitto.org"
keepalive=60
port=1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)
	
def on_publish(client, userdata, mid):
	print("Send succesed: " + userdata)
	
#=================================================
# main 
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(server, port, keepalive)

client.loop_start()
while True:
    sensor_data = random.randint(0,10)
    client.publish(topic, sensor_data)
    print("send: "+str(sensor_data))
    time.sleep(2)
  
"""
#================================================
# This module provides some helper functions to allow straightforward publishing of messages in a one-shot manner. In other words, they are useful for the situation where you have a single/multiple messages you want to publish to a broker, then disconnect with nothing else required.
# Publish a single message to a broker, then disconnect cleanly.
# .single(topic, payload=None, qos=0, retain=False, hostname="localhost", port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
publish.single(topic, "payload", hostname=server)

# Publish multiple messages to a broker, then disconnect cleanly.
# .multiple(msgs, hostname="localhost", port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
# The dict must be of the form: msg = {‘topic’:”<topic>”, ‘payload’:”<payload>”, ‘qos’:<qos>, ‘retain’:<retain>}
msgs = [{'topic':"test/topic", 'payload':"multiple 1"},("test/topic", "multiple 2", 0, False)]
publish.multiple(msgs, hostname=server)
"""  