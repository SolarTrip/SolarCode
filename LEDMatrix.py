# -*- encoding: utf-8 -*-

# (C) 2018 by Oliver Kuhlemann
# Bei Verwendung freue ich mich über Namensnennung,
# Quellenangabe und Verlinkung
# Quelle: http://cool-web.de/raspberry/

import RPi.GPIO as GPIO      # Funktionen für die GPIO-Ansteuerung laden
from time import sleep       # damit müssen wir nur noch sleep() statt time.sleep schreiben
from sys import exit         # um das Programm ggf. vorzeitg zu beenden

GPIO.setmode(GPIO.BCM)       # die GPIO-Pins im BCM-Modus ansprechen

PinData=11
PinClockStore=13
PinClockShift=15

GPIO.setup(PinData, GPIO.OUT)
GPIO.setup(PinClockStore, GPIO.OUT)
GPIO.setup(PinClockShift, GPIO.OUT)


ClockPulseLen=.0000001    # als HighSpeed-Baustein verträgt der HC595 auch kürzere Impulse

  
def delayMicroseconds(usecs):
   sleep (usecs/1000000);

def delay(msecs):
   sleep (msecs/1000);

   
def storeTick():    # einen Puls auf die ClockStore-Leitung schicken
   GPIO.output(PinClockStore, GPIO.HIGH)
   sleep (ClockPulseLen)
   GPIO.output(PinClockStore, GPIO.LOW)
   sleep (ClockPulseLen)


def shiftTick():    # einen Puls auf die ClockShift-Leitung schicken
   GPIO.output(PinClockShift, GPIO.HIGH)
   sleep (ClockPulseLen)
   GPIO.output(PinClockShift, GPIO.LOW)
   sleep (ClockPulseLen)
   
  
def clearDots(): # alle Punkte löschen
   for i in range(0,16):
      GPIO.output(PinData, GPIO.LOW)
      shiftTick() # nächstes Bit   
   storeTick()    # alle Bits fertig. Speichern



def lightCol(col, colByte): # Vorwiderstände hängen an den Row-Ausgängen, sonst keine gleichmäßige Helligkeit
   # zuerst das rowByte einschieben
  for b in range (0,8):
      w = (colByte & 1) 
      GPIO.output(PinData,w)           # w = 0 | 1
      shiftTick()                      # nächstes Bit   
      colByte = colByte >> 1                    

  # dann das colByte invertiert
  for b in range (0,8):
     w = (b == (7-col)) 
     w^=1   # invertieren, weil wird müssen auf Low und damit zu GND durchschalten
     GPIO.output(PinData,w)           # w = 0 | 1
     shiftTick()                      # nächstes Bit   

  storeTick()     # alle Bits fertig. Speichern


def lightDot(x, y):      # eine einzelne LED leuchten lassen
   lightCol(x, 1<<(7-y)) 


def lightMatrix( rowArray,  msecs):  # eine 8x8 Matrix leuchten lassen
   
   colArray = [0, 0, 0, 0, 0, 0, 0, 0]
   
   # übergeben wurden 8 Zeilen, diese auf 8 Spalten ummünzen, weil wir spaltenorientiert sind
   for col in range (0,8):
      for row in range (0,8):
         colArray[col] += (rowArray[7-row] & 128)/128 * (1 << row) 
         rowArray[7-row] = rowArray[7-row]<<1 
      
   # nun die Spalten anzeigen
   for i in range (0,msecs/7):
      for col in range (0,8):
         lightCol(col, colArray[col]) 
         delayMicroseconds(50) 

   clearDots() 


def scrollShow (colArray, verzoegerung):  # einen Scroll-Frame für eine bestimme Zeit anzeigen
   for i in range(0,verzoegerung/7):      
      for col in range (0,8):
         lightCol(col, colArray[col]) 
         delayMicroseconds(500) 
      clearDots() 


def scroll (text,  cols,  verzoegerung): # cols=Anzahl von Spalten gesamt - Scroller anzeigen
   
   colArray = [0, 0, 0, 0, 0, 0, 0, 0 ]
   
   #ersten Screen reinschieben
   for c in range (0,7):   
      for i in range (0,7):
         colArray[i]=colArray[i+1] 
      
      colByte=0 
      for row in range(0,8):
         if (text[row][c] == '#'):
            colByte += 1<<(7-row) 
      colArray[7]=colByte 
      scrollShow(colArray,verzoegerung)    
   
   # gesamten Text durchscrollen
   for col in range ( 0,cols-8):
      for c in range (col,col+8): # 8 ZeilenBytes holen
         colByte=0 
         for row in range (0,8):
            if (text[row][c] == '#'):
                colByte += 1<<(7-row) 
         
         colArray[c-col] = colByte 
      scrollShow(colArray,verzoegerung)    
   
   # letzten Screen auch noch rausschieben
   for c in range (0,8):   
      for i in range (0,7):
         colArray[i]=colArray[i+1] 
      colArray[7]=0 
      scrollShow(colArray,verzoegerung)    
   


# --- Ende Funktionen --- Beginn Hauptprogramm -------------------------------------------

#           1.  2.  3.  4.  5.  6.  7.  8.
#
# Anodes:    9, 14,  8, 12,  1,  7,  2,  5  ROW
# Cathodes: 13,  3,  4, 10,  6, 11, 15, 16  COL

#          74HC595                          74HC595       
# 
#  .--- 7 6 5 4 3 2 1 0 <--- Shift       F E D C B A 9 8 <---.  Bits
#  `---------------------------------------------------------´
                                                     

try:

   clearDots();

   ###### die Dots der Reihe nach durchschalten #####
   
   for i in range (0,64):
      x=i%8
      y=i/8
      lightDot(x,y)
      sleep (.025)
  

   clearDots();
   delay (500);

   ###### kleine Warte-Animation #####
   #   0 1 2 3 4 5 6 7
   #   . . # # # # . .  0
   #   . # . . . . # .  8
   #   # . . . . . . #  16
   #   # . . . . . . #  24
   #   # . . . . . . #  32
   #   # . . . . . . #  40
   #   . # . . . . # .  48 
   #   . . # # # # . .  56
   #
   
   
   dots = [2,3,4,5, 14, 23, 31, 39, 47, 54, 61,60,59,58, 49, 40, 32, 24, 16, 9]
   
   for w in range (0,10):
      for i in range (0,20):
         x=dots[i]%8
         y=dots[i]/8
         lightDot(x,y)
         sleep(.010)

   clearDots();
   delay(500);

   ###### ein 8x8-Matrix-Bild anzeigen #####
   
   pic = [0b01100110,
          0b10011001,
          0b10000001,
          0b10000001,
          0b10000001,
          0b01000010,
          0b00100100,
          0b00011000]

   lightMatrix (pic,2000)

   clearDots()
   delay (500)
   
   ###### einen Scroll-Text durchlaufen lassen #####
   
   scrollText = [
   "###...##.##....####....####....####...#..............#...#...#####..####.......####....#####",
   ".#...#..#..#..#....#..#....#..#....#..#..............#...#...#......#...#......#...#...#....",
   ".#...#.....#..#.......#....#..#....#..#..............#...#...#......#...#......#....#..#....",
   ".#...#.....#..#.......#....#..#....#..#......#####...#...#...####...####.......#....#..####.",
   ".#...#.....#..#.......#....#..#....#..#..............#...#...#......#...#......#....#..#....",
   ".#....#...#...#.......#....#..#....#..#..............#.#.#...#......#...#......#....#..#....",
   ".#.....#.#....#....#..#....#..#....#..#..............##.##...#......#...#..##..#...#...#....",
   "###.....#......####....####....####...#####..........#...#...#####..####...##..####....#####"
   ]

   scroll (scrollText,92,100)
   
   delay (500);
   clearDots();

         
except KeyboardInterrupt:
   pass

clearDots()
GPIO.cleanup()                  # Programm sauber verlassen und Ressourcen wieder freigeben