from machine import Pin
from time import sleep, time

motorSequence = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[1,0,0,1],]
motorPins1 = [Pin(2,Pin.OUT), Pin(15,Pin.OUT), Pin(27,Pin.OUT), Pin(25,Pin.OUT)]
motorPins2 = [Pin(26,Pin.OUT), Pin(33,Pin.OUT), Pin(14,Pin.OUT), Pin(13,Pin.OUT)]

def moveCoil(motorNumber):
    start_time = time()
    if motorNumber == 1:
        motorPins = motorPins1
    if motorNumber == 2:
        motorPins = motorPins2
    spin = True

    while spin:
        for step in motorSequence:
            for i in range(len(motorPins)):
                motorPins[i].value(step[i])
                sleep(0.001)
        if time() - start_time >= 3:
            spin = False 