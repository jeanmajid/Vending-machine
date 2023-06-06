import machine


class Apin:
    def __init__(self, pin_num):
        self.out = machine.ADC(machine.Pin(pin_num))

    def read(self):
        return self.out.read()

    def read_and_display(self):
        value = self.out.read()
        print(f"Kanal: {value}, Volt: {3.3 * (value / 4095):.2f}")
        return value

