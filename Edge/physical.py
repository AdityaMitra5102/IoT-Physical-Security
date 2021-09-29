import serial

def writeToArduino():
  for i in range(9):
    try:
      ser=serial.Serial('/dev/ttyUSB'+str(i),9600)
      ser.write(b'1')
    except:
      pass
