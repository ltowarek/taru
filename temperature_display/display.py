#!/usr/bin/env python3

from RPLCD.i2c import CharLCD

if __name__ == '__main__':
    temperature_outside = 10.5
    temperature_inside = 20.4
    degree_symbol = chr(223)
    lcd = CharLCD('PCF8574', 0x27)
    lcd.write_string('Out: {0}{2}C\n\rIn: {1}{2}C'.format(temperature_outside,
                                                          temperature_inside,
                                                          degree_symbol))
    lcd.close()
