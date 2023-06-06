from machine import Pin
from time import sleep

IN1 = Pin(2,Pin.OUT)
IN2 = Pin(15,Pin.OUT)
IN3 = Pin(27,Pin.OUT)
IN4 = Pin(25,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[1,0,0,1],]

while True:
    for step in sequence:
        for i in range(len(pins)):
            pins[i].value(step[i])
            sleep(0.001) # maximale Geschwindigkeit. sleep > 0.001 funktioniert nicht