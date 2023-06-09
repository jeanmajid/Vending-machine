from machine import Pin 
import time

PirSensor = Pin(23, Pin.IN)
lastDetect = False

def motion_det(): 
    if PirSensor.value() == 1 and lastDetect == False:
        lastDetect = True
        return True
    if PirSensor.value() == 0 and lastDetect == True:
        lastDetect = False
        return False

while True:
    motion_det()