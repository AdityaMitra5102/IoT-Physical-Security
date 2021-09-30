import serial
import time

def writeToArduino():
  for i in range(9):
    try:
      ser=serial.Serial('/dev/ttyUSB'+str(i),9600)
      time.sleep(3)
      ser.write(b'1')
    except:
      pass
