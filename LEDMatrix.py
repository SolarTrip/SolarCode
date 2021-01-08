import RPi.GPIO as GPIO
import time
LSBFIRST = 1
MSBFIRST = 2
dataPin   = 11    #DS Pin of 74HC595(Pin14)
latchPin  = 13    #ST_CP Pin of 74HC595(Pin12)
clockPin = 15    #CH_CP Pin of 74HC595(Pin11)

def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(dataPin, GPIO.OUT)
  GPIO.setup(latchPin, GPIO.OUT)
  GPIO.setup(clockPin, GPIO.OUT)

def shiftOut(dPin,cPin,order,val):
  for i in range(0,8):
    GPIO.output(cPin,GPIO.LOW);
    if(order == LSBFIRST):
      GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
    elif(order == MSBFIRST):
      GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
    GPIO.output(cPin,GPIO.HIGH);

def loop():
  while True:
    x=0x01
    for i in range(0,8):
      GPIO.output(latchPin,GPIO.LOW)
      shiftOut(dataPin,clockPin,LSBFIRST,x)
      GPIO.output(latchPin,GPIO.HIGH)
      x<<=1
      time.sleep(0.1)
    x=0x80
    for i in range(0,8):
      GPIO.output(latchPin,GPIO.LOW)
      shiftOut(dataPin,clockPin,LSBFIRST,x)
      GPIO.output(latchPin,GPIO.HIGH)
      x>>=1
      time.sleep(0.1)

def destroy(): 
  GPIO.cleanup()
if __name__ == '__main__':
  print ('Program is starting...' )
  setup() 
  try:
    loop()  
  except KeyboardInterrupt:  
    destroy() 