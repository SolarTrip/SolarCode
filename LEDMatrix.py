#!/usr/bin/env python3
#############################################################################
# Filename    : LEDMatrix.py
# Description : Control LEDMatrix with 74HC595
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

# define the pins connect to 74HC595
dataPin   = 11      # DS Pin of 74HC595(Pin14)
latchPin  = 13      # ST_CP Pin of 74HC595(Pin12)
clockPin = 15       # SH_CP Pin of 74HC595(Pin11)
pic = [0x1c,0x22,0x51,0x45,0x45,0x51,0x22,0x1c]  # data of smiling face
data = [     # data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # " "
    0x00, 0x66, 0x99, 0x81, 0x42, 0x24, 0x18, 0x00, # "heart"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00, # "1"
]
def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    

def loop():
    while True:
        for j in range(0,500): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPin,GPIO.LOW)
                
                GPIO.output(latchPin,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                time.sleep(0.001) # display the next column
                x>>=1
        for k in range(0,len(data)-8): #len(data) total number of "0-F" columns 
            for j in range(0,20): # times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x=0x80      # Set the column information to start from the first column
                for i in range(k,k+8):
                    GPIO.output(latchPin,GPIO.LOW)
                    GPIO.output(latchPin,GPIO.HIGH)
                    time.sleep(0.001)
                    x>>=1
def destroy():  
    GPIO.cleanup()
if __name__ == '__main__':  # Program entrance
    print ('Program is starting...' )
    setup() 
    try:
        loop()  
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()  

