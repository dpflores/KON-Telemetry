from curses import baudrate
import serial
import os,time
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


#os.system("stty -F /dev/ttyUSB2 -echo")
#time.sleep(5)
#os.system ("cat /dev/ttyUSB2&")
#time.sleep(5)
#os.system('echo AT > /dev/ttyUSB2')
#os.system('echo "AT+CGPS=1,1" > /dev/ttyUSB2')
#time.sleep(2)
#os.system('killall cat')
#time.sleep(2)
#os.system('echo "AT+CGPS?" > /dev/ttyUSB2')
#time.sleep(2)
#ser = serial.Serial("/dev/ttyUSB1")
#ser = serial.Serial("/dev/ttyUSB1")
#receiverd_data= (ser.readline())
#while ():
#    ser = serial.Serial("/dev/ttyUSB1")
#    while (receiverd_data == b'$GPGGA,,,,,,0,,,,,,,,*66\r\n' ):
#    receiverd_data= (ser.readline())
#    time.sleep(1)

#print(ser)
#out = 0
#while (out != 1):
#     ser = serial.Serial("/dev/ttyUSB1")
#     receiverd_data= (ser.readline()) 
#     GPGGA_Data = receiverd_data.find(b"$GPGGA,")
#     print(receiverd_data)
#     if (GPGGA_Data==0):
#          lat_flag=   receiverd_data.split(b",")[2]
#          print("conectando gpgga")
#          if lat_flag != b'':
#               out = 1
#               print("conectado")
               
ser = serial.Serial("/dev/ttyUSB1")
while True:
   
     receiverd_data= (ser.readline())   
     print(receiverd_data)
     GPGGA_Data = receiverd_data.find(b"$GPGGA,")
     GPVTG_Data = receiverd_data.find(b"$GPVTG,")
     print (GPGGA_Data)
     if (GPGGA_Data==0):
       
       lat,NorS,Lon,EorW= receiverd_data.split(b",")[2:6]
       Alt = receiverd_data.split(b",")[9]
       print(lat,NorS,Lon,EorW)
       if ((lat ==  b'') or ( Lon == b'')):
            print("Conectando...")
            time.sleep(2)
            
       else:
           
            posLat = round(convert_to_degrees(lat,NorS),6)
            posLon = round(convert_to_degrees(Lon,EorW),6)
            altitude = float(Alt)
            print(posLat, posLon,altitude)
    
    
     if (GPVTG_Data==0):
       speed = receiverd_data.split(b",")[7]
       if speed != b'':           
            print(float(speed))
       else:
            print("Conectando...")
            time.sleep(2)



