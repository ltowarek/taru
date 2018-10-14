#!/usr/bin/env python3

from RPLCD.i2c import CharLCD


class LCD:
    def __init__(self):
        self.lcd = None

    def open(self):
        self.lcd = CharLCD('PCF8574', 0x27)

    def close(self):
        self.lcd.close(clear=True)

    def print_temperature(self, outside, inside):
        degree_symbol = chr(223)
        self.lcd.write_string(
            'Out: {0}{2}C\n\rIn: {1}{2}C'.format(outside,
                                                 inside,
                                                 degree_symbol))

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    temperature_outside = 10.5
    temperature_inside = 20.4
    lcd = LCD()
    with lcd:
        lcd.print_temperature(temperature_outside, temperature_inside)

