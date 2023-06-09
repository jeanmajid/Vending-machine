I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

last_lcd_state = 0

def clearTopRow(lcd):
    lcd.move_to(0,0)
    lcd.putstr("                ")
    lcd.move_to(0,0)

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
