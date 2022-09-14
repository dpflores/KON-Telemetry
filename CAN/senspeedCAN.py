from asyncio import all_tasks
from curses import baudrate
from readline import set_completer_delims
import serial
import os,time
import socket
import struct

can_frame_fmt = "=IB3x8s";
can_frame_size = struct.calcsize (can_frame_fmt)

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def convert_to_degrees(raw_data,quadrant):
    float_Data= float(raw_data)
    decimal_value = float_Data/100
    degrees = int(decimal_value)
    minutes= (decimal_value - int(decimal_value))/0.6
    if (quadrant == b'W' or quadrant == b'S'):   
        position = (degrees + minutes)*(-1)
        return position
    else:
        position = (degrees + minutes)
        return position

s = socket.socket (socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(("can0",))                
ser = serial.Serial("/dev/ttyUSB1")
while True:
   
     receiverd_data= (ser.readline())   
     #print(receiverd_data)
     GPGGA_Data = receiverd_data.find(b"$GPGGA,")
     GPVTG_Data = receiverd_data.find(b"$GPVTG,")
     #print (GPGGA_Data)
     if (GPGGA_Data==0):
       
       lat,NorS,Lon,EorW= receiverd_data.split(b",")[2:6]
       Alt = receiverd_data.split(b",")[9]
       print(lat,3,NorS,Lon,EorW)
       
       if ((lat ==  b'') or ( Lon == b'')):
            print("Conectando...")
            time.sleep(2)
            
       else:
           
            posLat = round(convert_to_degrees(lat,NorS),6)
            posLon = round(convert_to_degrees(Lon,EorW),6)
            altitude = float(Alt)
            s.send(build_can_frame(0x10, Alt))
            print(posLat, posLon,altitude)
    
    
     if (GPVTG_Data==0):
       speed = receiverd_data.split(b",")[7]
       if speed != b'':           
            print(speed)
            
       else:
            print("Conectando...")
            time.sleep(2)