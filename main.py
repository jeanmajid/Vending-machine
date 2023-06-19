from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep, time

ready = False
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

rows = [Pin(4), Pin(5), Pin(12), Pin(18)]
cols = [Pin(16), Pin(19), Pin(17), Pin(0)]

keys = {
    (0, 0): 'D',
    (0, 1): 'C',
    (0, 2): 'B',
    (0, 3): 'A',
    (1, 0): '#',
    (1, 1): '9',
    (1, 2): '6',
    (1, 3): '3',
    (2, 0): '0',
    (2, 1): '8',
    (2, 2): '5',
    (2, 3): '2',
    (3, 0): '*',
    (3, 1): '7',
    (3, 2): '4',
    (3, 3): '1',
}

for row_pin in rows:
    row_pin.init(mode=Pin.OUT)
for col_pin in cols:
    col_pin.init(mode=Pin.IN, pull=Pin.PULL_UP)

PirSensor = Pin(23, Pin.IN)

motorSequence = [[1,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],]
motorPins1 = [Pin(2,Pin.OUT), Pin(15,Pin.OUT), Pin(27,Pin.OUT), Pin(25,Pin.OUT)]
motorPins2 = [Pin(26,Pin.OUT), Pin(33,Pin.OUT), Pin(14,Pin.OUT), Pin(13,Pin.OUT)]

onePressed = False
twoPressed = False
cash = 0
last_lcd_state = 0
lastDetect = False

text = "Bitte waehle ein Produkt"
length = totalColumns - 1
displayLen = 0
delay = 0.1

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
        if time() - start_time >= 20:
            spin = False

def clearTopRow(lcd):
    lcd.move_to(0,0)
    lcd.putstr("                ")
    lcd.move_to(0,0)

def motion_det():
    global lastDetect
    if PirSensor.value() == 1 and lastDetect == False:
        lastDetect = True
        return True
    if PirSensor.value() == 0 and lastDetect == True:
        lastDetect = False
        return False

def numpad_detection():
    global rows
    global cols
    global onePressed
    global twoPressed
    for i, row_pin in enumerate(rows):
        row_pin.value(0)
        for j, col_pin in enumerate(cols):
            if not col_pin.value():
                key = keys.get((i, j), None)
                if cash > 0:
                    if key == "1":
                        onePressed = True
                    if key == "2":
                        twoPressed = True
                sleep(1)
        row_pin.value(1)

def lcd_if_cash():
    global last_lcd_state
    global text
    global displayLen
    global delay
    if last_lcd_state == 0:
        lcd.clear()
        lcd.move_to(0,1)
        lcd.putstr(" Geld: " + str(cash))
        lcd.move_to(0,0)
        displayLen = 0
        last_lcd_state = 1
    for l in text:
        if text[0] == l:
            clearTopRow(lcd)
            displayLen = 0
        sleep(delay)
        displayLen += 1
        lcd.putchar(l)
        if displayLen >= length:
            lcd.move_to(-1, 0)
            lcd.putchar(" ")
            displayLen = 0
            clearTopRow(lcd)

def lcd_default():
    global last_lcd_state
    if last_lcd_state == 1:
        lcd.clear()
        last_lcd_state = 0
    lcd.putstr("Waehl ein " + "      "+ "Produkt")
    lcd.clear()
    sleep(1)
    lcd.putstr("Wirf eine Münze ein")
    sleep(1)
    lcd.clear()

ready = True
while ready:
    if (motion_det()):
        cash += 1
    numpad_detection()
    if cash > 0:
        lcd_if_cash()
        if onePressed:
            moveCoil(1)
            cash -= 1
            onePressed = False
        elif twoPressed:
            moveCoil(2)
            cash -= 1
            twoPressed = False
    else:
        lcd_default()
