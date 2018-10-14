#!/usr/bin/env python3

from RPLCD.i2c import CharLCD


class LCD:
    DEGREE_SYMBOL = chr(223)

    def __init__(self):
        self.lcd = None

    def open(self):
        self.lcd = CharLCD('PCF8574', 0x27)

    def close(self):
        self.lcd.close(clear=True)

    def print_outside_temperature(self, temperature):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(
            'Out: {}{}C'.format(temperature, self.DEGREE_SYMBOL))

    def print_inside_temperature(self, temperature):
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(
            'In: {}{}C'.format(temperature, self.DEGREE_SYMBOL))

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    temperature_outside = 10.5
    temperature_inside = 20.4
    with LCD() as lcd:
        lcd.print_outside_temperature(temperature_outside)
        lcd.print_inside_temperature(temperature_inside)
