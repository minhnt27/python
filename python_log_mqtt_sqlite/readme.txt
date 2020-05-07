For study, 5/5-7/5/2020, by minhnt27

Test schema:
[GenMessage]--------[MqttBroker]----------[GetMessage_writeSQLite]----------[SQLite]---------[readSQLite_plotSignal]

[MqttBroker]: a online Mqtt Broker, can be: (5 OnlineMQTT Brokers  for Testing)
Broker			Server							Ports					Websocket
Mosquitto	 	iot.eclipse.org					1883 / 8883				n/a
HiveMQ	 		broker.hivemq.com				1883					8000
Mosquitto	 	test.mosquitto.org				1883 / 8883 / 8884		8080 / 8081
mosca	 		test.mosca.io					1883					80
HiveMQ	 		broker.mqttdashboard.com		1883	

[SQLite]: a DB be installed in local PC

[GenMessage]: a Python app to publish a random value (0-10) at interval 2s

[GetMessage_writeSQLite]:  a Python app to subcribe the same topic with [GenMassage], write timestap, topic, payload to [Sqlite]

[readSQLite_plotSignal]: a Python app to read only last 100 record (timestamp and payload) to plot a chart, update each 100s.
Note:For animate chart, it should run on interpreter 

