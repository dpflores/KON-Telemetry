import serial
import os,time
import webbrowser
import sys
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
    
#os.system('stty -F /dev/ttyUSB2 -echo')
#os.system ('cat /dev/ttyUSB2&')
#time.sleep(2)
#os.system('echo AT > /dev/ttyUSB2')
#os.system('echo "AT+CGPS=1,1" > /dev/ttyUSB2')
#time.sleep(2)
os.system('echo "AT+CGPS?" > /dev/ttyUSB2')
time.sleep(2)
ser = serial.Serial("/dev/ttyUSB1")
time.sleep(1)
GPGGA_Buffer = 0
try:
    while True:
        receiverd_data= ser.readline()
    
        GPGGA_Data = receiverd_data.find(b"$GPGGA,")
        GPVTG_Data = receiverd_data.find(b"$GPVTG,")
        #print(GPGGA_Data)
    
        if (GPGGA_Data==0):
       
            lat,NorS,Lon,EorW = receiverd_data.split(b",")[2:6]
            print(lat,NorS,Lon,EorW)
            if ((lat !=  b'') or ( Lon != b'')):
                posLat = convert_to_degrees(lat,NorS)
                posLon = convert_to_degrees(Lon,EorW)
                print(posLat, posLon)
                map_link = 'http://maps.google.com/?q=' + str(posLat) + ','+str(posLon)
                print("press ctrl+c \n")
            else:
                print("Obteniendo valores de coordenadas...")
                time.sleep(2)
    
    
        if (GPVTG_Data==0):
           
            if speed != b'':
                speed = receiverd_data.split(b",")[7]
                print(float(speed))
            else:
                print("Obteniendo valo de velocidad")
                time.sleep(2)
except KeyboardInterrupt:
    webbrowser.open(map_link)
    sys.exit(0)

