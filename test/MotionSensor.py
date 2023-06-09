from machine import Pin 
import time

PirSensor = Pin(23, Pin.IN)
lastDetect = False

def motion_det(): 
    if PirSensor.value() == 1 and lastDetect == False:
        print("motion detected")
        lastDetect = True
        time.sleep(0.5) 
    if PirSensor.value() == 0 and lastDetect == True:
        print("no motion")
        lastDetect = False
        time.sleep(0.5)

while True:
    motion_det()