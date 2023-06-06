import machine


class Led:
    def __init__(self, pin_num):
        self.led = machine.Pin(pin_num, machine.Pin.OUT)

    def on(self):
        self.led.value(1)

    def off(self):
        self.led.value(0)

    def switch(self):
        if self.value() == 1:
            self.value(0)
        elif self.value() == 0:
            self.value(1)
