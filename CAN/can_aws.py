import socket
import struct
import paho.mqtt.client as mqtt
import os
import ssl
import random
import string
import json
from time import sleep
from random import uniform

connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS");
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str
    
def getMAC(interface='eth0'):
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]
def getEthName():
  # Get name of the Ethernet interface
  try:
    for root,dirs,files in os.walk('/sys/class/net'):
      for dir in dirs:
        if dir[:3]=='enx' or dir[:3]=='eth':
          interface=dir
  except:
    interface="None"
  return interface
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = mqtt.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a2s0sulx81fxaq-ats.iot.us-east-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "axotec1"                                     # Thing_Name
thingName = "axotec1"                                    # Thing_Name
caPath = "/home/pi/Desktop/AWS/Virginia/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "/home/pi/Desktop/AWS/Virginia/c2491d27e03f31fa51935eccdadd1900220517b6c58c4cb818d53cb92abc18a6-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/Desktop/AWS/Virginia/c2491d27e03f31fa51935eccdadd1900220517b6c58c4cb818d53cb92abc18a6-private.pem.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
                



can_frame_fmt = "=IB3x8s";
can_frame_size = struct.calcsize (can_frame_fmt)

def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame) 
    return (can_id, can_dlc, data[:can_dlc])

s = socket.socket (socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(("can0",))

while True:
    cf, addr = s.recvfrom(16)
    can_id = dissect_can_frame(cf)[0]
    if can_id == 259 :
        can_dlc = dissect_can_frame(cf)[1]
        dataL = hex((dissect_can_frame(cf)[2])[0])#Data LSB
        dataH = hex((dissect_can_frame(cf)[2])[1])#Data HSB
   
        #data= (int (dataH,16))<<8| int (dataL,16)
        data = int (dataH,16) + int (dataL,16)

        #print (dataL)
        #print(dataH )
        print (data)
        
        

        
        if connflag == True:
            ethName=getEthName()
            ethMAC=getMAC(ethName)
            macIdStr = ethMAC
            randomNumber = int (data)
            random_string= get_random_string(8)
            paylodmsg0="{"
            paylodmsg1 = "\"mac_Id\": \""
            paylodmsg2 = "\", \"Speed (rpm)\":"
            paylodmsg3 = ", \"random_string\": \""
            paylodmsg4="\"}"
            paylodmsg = "{} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, macIdStr, paylodmsg2, randomNumber, paylodmsg3, random_string, paylodmsg4)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("comunicacionaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg sent: comunicacionaws" ) # Print sent temperature msg on console
            print(paylodmsg_json)

        else:
            print("waiting for connection...")      
            