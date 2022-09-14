import time
import requests
import math
import random
import paho.mqtt.client as mqtt
import os
import socket
import ssl
import string
import json
from time import sleep
from random import uniform

from ubi_test import VARIABLE_LABEL_2


host = 'industrial.api.ubidots.com'
port = 1883
DEVICE_LABEL = 'pruebamqtt'
TOKEN= "BBFF-63z3UEvKXujfADnc061BnqyXrIxNWt"  # Put your TOKEN here
password=""
VARIABLE_LABEL_1 = "temperature"
VARIABLE_LABEL_2 = "current"


def build_payload(variable_1, variable_2):
    # Creates two random values for sending data
    value_1 = random.randint(-10, 50)
    value_2 = random.randint(0, 85)
    
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


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Attemping to send data")
    print(payload)
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)

