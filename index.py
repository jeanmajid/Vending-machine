from machine import Pin, I2C # Vo machine Pin und I2C importieren
from lcd_api import LcdApi # Von der lcd_api datei 
from i2c_lcd import I2cLcd
from time import sleep,time
ready = False # Die ready variable die False ist
# Lcd screen initzialiesieren
I2C_ADDR = 0x27 # Die addresse des LCD Bildschirms
totalRows = 2 # Die anzahl der rows
totalColumns = 16 # Die länge der rows

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000) # Definieren des LCD Displays mit den Pins und der frequenz
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns) # Definieren des LCD Displays mit der hex addresse und dem Rows und Colums
# Numpad initzialisieren
rows = [Pin(4), Pin(5), Pin(12), Pin(18)] # Die rows vom Numpad in einem array
cols = [Pin(16), Pin(19), Pin(17), Pin(0)] # Die colums vom Numpad in einem array

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
} # Keys tuple der alle key combis speichert (wie ein koordinatensystem)

for row_pin in rows: # Für jeden pin in dem rows array
    row_pin.init(mode=Pin.OUT) # Den Pin auf Output setzten
for col_pin in cols: # Für jeden pin in dem cols array
    col_pin.init(mode=Pin.IN, pull=Pin.PULL_UP) # Den pin auf input setzten mit pull_up (keine ahnung was das ist)
#sensor
PirSensor = Pin(23, Pin.IN) # Der Sensor der als input pin definiert wird
#Motor
motorSequence = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[1,0,0,1],] # Die sequenz wegen dem Motor
motorPins1 = [Pin(2,Pin.OUT), Pin(15,Pin.OUT), Pin(27,Pin.OUT), Pin(25,Pin.OUT)] # Die pins für den 1ten Motor
motorPins2 = [Pin(26,Pin.OUT), Pin(33,Pin.OUT), Pin(14,Pin.OUT), Pin(13,Pin.OUT)] # Die pins für den 2ten Motor
#Variablen
onePressed = False # Die variable die anzeigt ob eins auf dem numpad gedrückt wurde
twoPressed = False # Die variable die anzeigt ob zwei auf dem numpad gedrückt wurde
cash = 0 # Die variable die anzeigt wie viel guthaben der user hat
last_lcd_state = 0 # Die variable die dem code sagt welchen status der LCD zuletzt hatte
lastDetect = False # Die variable die anzeigt was als letztes vom sensor erkannt wurde
#LCD if_cash variablen
text = "Bitte waehle ein Produkt" # Der text der angezeigt wird während
length = totalColumns - 1 # Die variable die anzeigt wie lange der text in der oberen zeile sein darf
displayLen = 0 # Variable um die länge der oberen reihe anzuzeigen
delay = 0.1 # wie schnell die buchstaben erscheinen sollen
#Funktionen
def moveCoil(motorNumber):
    start_time = time() # Die lokale zeit des esp32 in der variable start_time speichern
    if motorNumber == 1: # Wenn die, mit der gerufenen motorNummer, 1 ist
        motorPins = motorPins1 # Die motorPins variable auf die Motor pins für den ersten Motor setzten
    if motorNumber == 2: # Wenn die, mit der gerufenen motorNummer, 2 ist
        motorPins = motorPins2 # Die motorPins variable auf die Motor pins für den zweiten Motor setzten
    spin = True # Spin auf True setzten um den While spin loop zu starten

    while spin: # While Loop, welche den Motor in Bewegung setzt
        for step in motorSequence: # For Loop für step in der Liste motorSequence
            for i in range(len(motorPins)): # For Loop in der range von der länge des motorPins arrays, i = (0, 3)
                motorPins[i].value(step[i]) # Der ausgewählte motorPin wird auf den value, des sequence arrays, objectes gestellt
                sleep(0.001)  # Maximum speed. sleep > 0.001 does not work
        if time() - start_time >= 3: # Gibt an wie lange sich der Motor dreht in sekunden wenn jetztige zeit - zeit zum startpunkt grösser als 3 ist
            spin = False # While loop stoppen

def clearTopRow(lcd):
    lcd.move_to(0,0) # Cursor auf die start position setzten
    lcd.putstr("                ") # Ein leeren 16 zeiligen string printen um die reihe zu clearen
    lcd.move_to(0,0) # Cursor auf die start position setzten

def motion_det():
    global lastDetect # Die globale variable lastDetect benutzten
    if PirSensor.value() == 1 and lastDetect == False: # wenn der sensor was erkennt ( hight gestellt ist )
        lastDetect = True # Die variable lastDetect auf True setzten damit der sensor nur noch low detecten kann
        return True # True returnen
    if PirSensor.value() == 0 and lastDetect == True: # wenn der sensor nichts erkennt ( low gestellt ist )
        lastDetect = False # Die variable lastDetect auf False setzten damit der sensor nur noch high detecten kann
        return False # False returnen

def numpad_detection():
    global rows # Die globale variable rows beuntzten
    global cols # Die globale variable cols bentzten
    global onePressed # Die globale variable onePressed bentzten
    global twoPressed # Die globale variable twoPressed benutzten
    for i, row_pin in enumerate(rows): # Ein for loop gestartet wo durch alle pins dem rows array geloopt wird mit deren index nummer i
        row_pin.value(0) # setzt alle pins in dem rows array zu low
        for j, col_pin in enumerate(cols): # Hier ist noch ein for loop in einem for loop dies nennt man nested loops. in diesem loop werden durch alle colum pins geloopt mit deren index wert
            if not col_pin.value(): # Kukt ob der colum pin nicht den wert 1 hat also 0 (low) und dann wurde erkannt das dieser knopf gedrückt wurde
                key = keys.get((i, j), None) # aus dem keys array werden jetzt der knopf mit den werten i und j gesucht welches die index werte für unser row und colum sind. wenn keins gefunden wurde dann gibt er None aus
                if cash > 0: # Kuken ob der benutzter mehr als 0 cash (Geld) hat
                    if key == "1": # Wenn der gedrückte key 1 ist
                        onePressed = True # Die globale variable onePressed wird auf True gesetzt
                    if key == "2": # Wenn der gedrückte key 2 ist
                        twoPressed = True # Die globale variable twoPressed wird auf True gesetzt            
                sleep(1) # sleep
        row_pin.value(1) # Diese linie gehört nicht mehr zum if und hat die aufgabe den row pin auf high zu stellen damit der nächste Pin kontroliert werden kann

def lcd_if_cash():
    global last_lcd_state # Die globale variable last_lcd_state benutzten
    global text # Die globale variable text benutzten
    global displayLen # Die globale variable für wie viele zeichen gearde in der oberen reihe sind
    global delay # wie schnell die buchstaben erscheinen sollen von der globalen variable nehmen
    if last_lcd_state == 0: # Kuken ob der lcd screen zuletzt den status 0 (default) hatte um zu kuken ob er ressetet werden muss
        lcd.clear() # LCD screen clearen
        lcd.move_to(0,1) # Pointer zur unteren zeile verschieben
        lcd.putstr(" Geld: " + str(cash)) # Geld in die untere zeile schreiben und ein abstand um ein problem zu beheben, weil die erste zeile von der 2 reihe wird gecleared (keine lust es zu beheben)
        lcd.move_to(0,0) # Cursor wieder auf den default platzt 0 0 packen
        displayLen = 0 # Display length resetten
        last_lcd_state = 1 # Die globale variable auf 1 setzten um zu signalieseiren das der screen gearde im cash mode ist
    for l in text: # durch jeden char im text loopen
        if text[0] == l: # Wenn der text die erste char ist dann
            clearTopRow(lcd) # Die obere reihe resetten
            displayLen = 0  # Die information der länge des displays auf null updaten
        sleep(delay) # Sleep
        displayLen += 1 # increment by one
        lcd.putchar(l) # Den char der gearde geloopt wird 
        if displayLen >= length: # überprüfen ob der string länger als die angegebene länge ist
            lcd.move_to(-1, 0) # Cursor auf die grundposition verschieben (-1 weil es bei 0 probleme gab)
            lcd.putchar(" ") # wenn ja den string links um ein kürzen
            displayLen = 0 # Die anzahl an zeichen wieder auf 0 setzten damit das Program weiß das er nurnoch 0 characktere hat
            clearTopRow(lcd) # clearTopRow funktion rufen welche die obere reihe leer macht

def lcd_default():
    global last_lcd_state # Die globale variable last_lcd_state benutzten
    if last_lcd_state == 1: # Kuken ob der lcd screen zuletzt den status 1 (if_cash) hatte um zu kuken ob er ressetet werden muss
        lcd.clear() # LCD screen clearen
        last_lcd_state = 0 # Die globale variable auf 0 setzten um zu signalieseiren das der screen gearde im default mode ist
    lcd.putstr("Waehl ein " + "      "+ "Produkt") # Auf den LCD printen das der user sich das der user ein Produkt wählen soll
    lcd.clear() # LCD screen clearen
    sleep(1) # sleep
    lcd.putstr("Wirf eine Münze ein") # Auf dem LCD printen das der user eine münze einwerfen soll
    sleep(1) # sleep
    lcd.clear() # Lcd screen clearen
ready = True # ready wird auf True gesetzt um zu signalisieren das der code bereit ist den main loop zu gehen
while ready: # Wenn ready True
    if (motion_det()): # Wenn Motion detection true returned
        cash += 1 # Cash 1 hoch setzten
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