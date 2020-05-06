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

import paho.mqtt.client as mqtt

#================================================
# test with topic "test/topic" on server "test.mosquitto.org"
topic="test/topic"
server="test.mosquitto.org"
port=1883
keepalive=60

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#=================================================
# main 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, port, keepalive)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()