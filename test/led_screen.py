
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

flow = False

lcd.move_to(0,1)
lcd.putstr(" Geld: ")
lcd.move_to(0,0)
flow = True

text = "Der Herbstwind wehte über den Spielplatz und drehte das kleine Stehkarussell wie von Geisterhand. Jan saß im Gras zwischen den gefallenen, braun gewordenen Blättern und rupfte einzelne Büschel samt der Wurzel aus der Erde. Maxi hing kopfüber vom Klettergerüst und zog Grimassen, die den vielen Erwachsenen galten, die ihn in seinem Leben enttäuscht hatten. Obwohl gerade Ferien waren, spielten die beiden allein. Einige der Jungs waren mit ihren Eltern in den Urlaub gefahren, andere aufgrund des schlechten Wetters Zuhause geblieben. Sobald man eine Jacke anziehen musste, um raus zu gehen, war der Sommer vorbei und damit all die wunderbaren Spiele, die er mit sich brachte. Für Jungs in ihrem Alter war der Herbst meist eine lästige Jahreszeit, eine Wartejahreszeit, zwischen der Hitze des Sommers und dem Schnee des Winters. Für Kastaniensammeln war man bereits viel zu alt und um nur noch drinnen abzuhängen,  zu jung. Der Himmel war von einer dicken Wolkendecke überzogen, die alles in ein schwermütiges Grau tauchte. Maxi schwang sich geschickt nach oben, griff mit seinen kleinen Armen eine Stange des Klettergerüsts, hielt sich einen Moment lang fest und ließ dann los. Er landete mit einem dumpfen Schlag auf dem frischen Rindenmulch. Dann ging er zu Jan rüber, der immer noch auf dem Boden hockte und gelangweilt zu den Feldern sah, wo das hohe Gras vom Wind wie Wellen erst in die eine, dann in die andere Richtung geworfen wurde. Maxi ließ sich ein Stück hinter ihm nieder und fing ebenfalls an, Gras aus dem Boden zu reißen und in den Wind zu werfen. Es wurde einige Meter durch die Luft getragen, bevor es in einem nahestehenden Busch hängen blieb. Ihre jungen Geister gaben sich nicht lange mit einer derartig eintönigen Beschäftigung zufrieden. Bald ließen sie vom Gras ab und starrten einfach nur geradeaus. Trotz der Langeweile kam es keinem der beiden in den Sinn nach Hause zu gehen. Allein die Möglichkeit eines bevorstehenden Abenteuers, rechtfertigte das nutzlose Rumhängen im kalten Wind. Nach einer kurzen Zeit des stillen Verharrens, förderte Maxi einen großen Klumpen Dreck aus der Erde und schmiß ihn auf Jan, der mit dem Gesicht zu den Feldern gewandt, nicht ausweichen konnte. Das Geschoss traf ihn direkt am Rücken, prallte von seiner grauen Regenjacke ab und landete hinter ihm auf dem Boden."
length = totalColumns - 1
displayLen = 0
delay = 0.1 # wie schnell die buchstaben erscheinen sollen

def clearTopRow(lcd):
    lcd.move_to(0,0)
    lcd.putstr("                ")
    lcd.move_to(0,0)

while flow:
    for l in text:
        if text[0] == l:
           clearTopRow(lcd)
           displayLen = 0
        sleep(delay)
        displayLen += 1
        lcd.putchar(l)
        if displayLen >= length: # überprüfen ob der string länger als die angegebene länge ist
            lcd.move_to(-1, 0)
            lcd.putchar(" ") # wenn ja den string links um ein kürzen
            displayLen = 0
            clearTopRow(lcd)


