import socket
import struct
import paho.mqtt.client as mqtt
import os
import ssl
import random
import string
import json
from time import sleep
from random import randint, randrange, uniform
import time
import requests
import math





 
#########################################################
                
TOKEN = # Put your TOKEN here
DEVICE_LABEL = "prueba"  # Put your device label here 
VARIABLE_LABEL_1 = "speed"  # Put your first variable label here
VARIABLE_LABEL_2 = "current"  # Put your second variable label here

def build_payload(variable_1, variable_2, value_1, value_2):    
    
    payload = {variable_1: value_1,
                variable_2: value_2}   

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def send_ubi(value_1, value_2):
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, value_1,value_2)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

#################################################


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
        data2=randint(2,10)
        send_ubi(data2, data2)
        #print (dataL)
        #print(dataH )
        print (data2)
        
        

        
  
            
