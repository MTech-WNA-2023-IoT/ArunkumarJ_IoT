import paho.mqtt.client as paho
import pymysql

global mqttclient;
global broker;
global port;



broker = "0.0.0.0";
port = 1883;

client_uniq = "pubclient_123"

mqttclient = paho.Client(client_uniq, True) 

def test(client, userdata, message):
  print("client:"+ str(client))
  print("userdata:"+ str(userdata))
  print("message:"+ str(message.payload))
  payload=float(message.payload)
  conn =pymysql.connect(database="IOTData",user="pi",password="raspberry",host="localhost")
  #Create a MySQL Cursor to that executes the SQLs
  cur=conn.cursor()
  #Create a dictonary containing the fields, name, age and place
  data={'topic':'SENSOR/TEMP','data':message.payload}
  #Execute the SQL to write data to the database
  cur.execute("INSERT INTO `MQTTData`(`Topic`,`MyData`)VALUES(%(topic)s,%(data)s);",data)
  #Close the cursor
  #cur.close()
  #Commit the data to the database
  conn.commit()



def _on_message(client, userdata, msg):
# 	print("Received: Topic: %s Body: %s", msg.topic, msg.payload)
	print(msg.topic+" "+str(msg.payload))
	


	 
#Subscribed Topics 
def _on_connect(mqttclient, userdata, flags, rc):
# 	print("New Client: "+str(mqttclient)+ " connected")
# 	print(rc)
	mqttclient.subscribe("SENSOR/#", qos=0)	
  
mqttclient.message_callback_add("SENSOR/TEMP", test)

mqttclient.connect(broker, port, keepalive=1, bind_address="")
  
mqttclient.on_connect = _on_connect

mqttclient.loop_forever()
conn.close()
