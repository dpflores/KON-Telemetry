# importing libraries
import paho.mqtt.client as mqtt
import os
import socket
import ssl
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )                              # Subscribe to all topics
 
def on_message(client, userdata, msg):                      # Func for receiving msgs
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))
 
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = mqtt.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost =  # Endpoint
awsport = 8883                                              # Port no.   
clientId = "axotec1"                                     # Thing_Name
thingName = "axotec1"                                    # Thing_Name
caPath = "/home/pi/Desktop/AWS/Virginia/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "/home/pi/Desktop/AWS/Virginia/c2491d27e03f31fa51935eccdadd1900220517b6c58c4cb818d53cb92abc18a6-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/Desktop/AWS/Virginia/c2491d27e03f31fa51935eccdadd1900220517b6c58c4cb818d53cb92abc18a6-private.pem.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop

