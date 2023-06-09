from machine import Pin
from time import sleep

rows = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(12, Pin.OUT), Pin(18, Pin.OUT)]
cols = [Pin(16, Pin.IN), Pin(19, Pin.IN), Pin(17, Pin.IN), Pin(0, Pin.IN)]

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
for row_pin in rows: # Für jeden pin in dem rows array
    row_pin.init(mode=Pin.OUT) # Den Pin auf Output setzten
for col_pin in cols: # Für jeden pin in dem cols array
    col_pin.init(mode=Pin.IN, pull=Pin.PULL_UP) # Den pin auf input setzten mit pull_up (keine ahnung was das ist)
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