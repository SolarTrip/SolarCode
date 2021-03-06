import RPi.GPIO as GPIO
import time
LSBFIRST = 1
MSBFIRST = 2
dataPin   = 11    #DS Pin of 74HC595(Pin14)
latchPin  = 13    #ST_CP Pin of 74HC595(Pin12)
clockPin = 15    #CH_CP Pin of 74HC595(Pin11)

data = [0x00,0x66,0x99,0x81,0x42,0x24,0x18,0x00,
        0x00,0x66,0xff,0xc3,0x42,0x24,0x18,0x00,
        0x00,0x66,0xff,0xe7,0x66,0x3c,0x18,0x00,
        0x00,0x66,0xff,0xff,0x7e,0x3c,0x18,0x00,
        
]




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
        for j in range(0,500): # Repeat enough times to display the smiling face a period of time
            x=0x20
            for i in range(0,8):
                GPIO.output(latchPin,GPIO.LOW)
                shiftOut(dataPin,clockPin,LSBFIRST,x) #first shift data of line information to first stage 74HC959

                shiftOut(dataPin,clockPin,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                GPIO.output(latchPin,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                time.sleep(0.001) # display the next column
                x>>=1
        for k in range(0,len(data)-8): #len(data) total number of "0-F" columns 
            for j in range(0,20): # times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x=0x80      # Set the column information to start from the first column
                for i in range(k,k+8):
                    GPIO.output(latchPin,GPIO.LOW)
                    shiftOut(dataPin,clockPin,MSBFIRST,data[i])
                    shiftOut(dataPin,clockPin,LSBFIRST,~x)
                    GPIO.output(latchPin,GPIO.HIGH)
                    time.sleep(0.001)
                    x>>=1

def destroy(): 
  GPIO.cleanup()
if __name__ == '__main__':
  print ('Program is starting...' )
  setup() 
  try:
    loop()  
  except KeyboardInterrupt:  
    destroy() 