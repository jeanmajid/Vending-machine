from machine import Pin, I2C
from time import sleep

PirSensor = Pin(23, Pin.IN)

def motion_det():
    if PirSensor.value() == 1:  
        return True
    if PirSensor.value() == 0:
        return False
    
while True:
    print(motion_det())
    sleep(1)
