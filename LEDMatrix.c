/**********************************************************************
* Filename    : LEDMatrix.c
* Description : Control LEDMatrix by 74HC595
* Author      : www.freenove.com
* modification: 2019/12/27
**********************************************************************/
#include <wiringPi.h>
#include <stdio.h>
#include <wiringShift.h>

#define   dataPin   0   //DS Pin of 74HC595(Pin14)
#define   latchPin  2   //ST_CP Pin of 74HC595(Pin12)
#define   clockPin 3    //SH_CP Pin of 74HC595(Pin11)
// data of smile face
unsigned char pic[]={0x1c,0x22,0x51,0x45,0x45,0x51,0x22,0x1c
                     0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff};
unsigned char data[]={  // data of "0-F"
    
};
void _shiftOut(int dPin,int cPin,int order,int val){   
	int i;  
    for(i = 0; i < 8; i++){
        digitalWrite(cPin,LOW);
        if(order == LSBFIRST){
            digitalWrite(dPin,((0x01&(val>>i)) == 0x01) ? HIGH : LOW);
            delayMicroseconds(10);
		}
        else {//if(order == MSBFIRST){
            digitalWrite(dPin,((0x80&(val<<i)) == 0x80) ? HIGH : LOW);
            delayMicroseconds(10);
		}
        digitalWrite(cPin,HIGH);
        delayMicroseconds(10);
	}
}
int main(void)
{
    int i,j,k;
    unsigned char x;
    
    printf("Program is starting ...\n");
    
    wiringPiSetup();
    
    pinMode(dataPin,OUTPUT);
    pinMode(latchPin,OUTPUT);
    pinMode(clockPin,OUTPUT);
    while(1){
        for(j=0;j<500;j++){  //Repeat enough times to display the smiling face a period of time
            x=0x80;
            for(i=0;i<8;i++){
                digitalWrite(latchPin,LOW);
                _shiftOut(dataPin,clockPin,MSBFIRST,pic[i]);// first shift data of line information to the first stage 74HC959
                _shiftOut(dataPin,clockPin,MSBFIRST,~x);//then shift data of column information to the second stage 74HC959

                digitalWrite(latchPin,HIGH);//Output data of two stage 74HC595 at the same time
                x>>=1;   //display the next column
                delay(1);
            }
        }
        for(k=0;k<sizeof(data)-8;k++){  //sizeof(data) total number of "0-F" columns 
            for(j=0;j<20;j++){  //times of repeated displaying LEDMatrix in every frame, the bigger the “j”, the longer the display time 
               x=0x80;          //Set the column information to start from the first column
                for(i=k;i<8+k;i++){
                    digitalWrite(latchPin,LOW);
                    _shiftOut(dataPin,clockPin,MSBFIRST,data[i]);
                    _shiftOut(dataPin,clockPin,MSBFIRST,~x);
                    digitalWrite(latchPin,HIGH);
                    x>>=1;
                    delay(1);
                }
            }
        }
    }
    return 0;
}


