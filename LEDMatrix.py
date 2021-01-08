#!/usr/bin/env python3
#############################################################################
# Filename    : LEDMatrix.py
# Description : Control LEDMatrix with 74HC595
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins connect to 74HC595
dataPin   = 11      # DS Pin of 74HC595(Pin14)
latchPin  = 13      # ST_CP Pin of 74HC595(Pin12)
clockPin = 15       # SH_CP Pin of 74HC595(Pin11)
const byte IMAGES[][8] = {
{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00001100,
  B00011110,
  B00111110,
  B01111100,
  B01111100,
  B00111110,
  B00011110,
  B00001100
},{
  B00000000,
  B00011000,
  B00111100,
  B01111110,
  B11111111,
  B11111111,
  B01100110,
  B00000000
},{
  B00110000,
  B01111000,
  B01111100,
  B00111110,
  B00111110,
  B01111100,
  B01111000,
  B00110000
},{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B00110011,
  B01111111,
  B01111111,
  B00111111,
  B00011110,
  B00001100,
  B00000000
},{
  B00000000,
  B00011001,
  B00111111,
  B00111111,
  B00011111,
  B00001111,
  B00000110,
  B00000000
},{
  B00000000,
  B00001100,
  B00011111,
  B00011111,
  B00001111,
  B00000111,
  B00000011,
  B00000000
},{
  B00000000,
  B00000110,
  B00001111,
  B00001111,
  B00000111,
  B00000011,
  B00000001,
  B00000000
},{
  B00000000,
  B00000011,
  B00000111,
  B00000111,
  B00000011,
  B00000001,
  B00000000,
  B00000000
},{
  B00000000,
  B00000001,
  B00000011,
  B00000011,
  B00000001,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000001,
  B00000001,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00010000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00010000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00010000,
  B00010000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00011000,
  B00010000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00011000,
  B00011000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00011000,
  B00011000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00011000,
  B00111100,
  B00111100,
  B00011000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00011000,
  B00111100,
  B00111100,
  B00011000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00111100,
  B00111100,
  B00111100,
  B00111100,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B01111110,
  B01111110,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B00000000,
  B01111110,
  B01111110,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
},{
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000,
  B00000000
},{
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000,
  B00000000,
  B00000000
},{
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B01111110,
  B00111100,
  B00011000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00111100,
  B00011000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00011000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
},{
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
}};
const int IMAGES_LEN = sizeof(IMAGES)/8;

def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
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
        for j in range(0,500): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPin,GPIO.LOW)
                shiftOut(dataPin,clockPin,MSBFIRST,pic[i]) #first shift data of line information to first stage 74HC959

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
                    shiftOut(dataPin,clockPin,MSBFIRST,~x)
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

