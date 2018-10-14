from RPLCD.i2c import CharLCD

if __name__ == '__main__':
    temperature_outside = 10
    temperature_inside = 20
    lcd = CharLCD('PCF8574', 0x27)
    lcd.write_string(f'Out: {temperature_outside}\u2103\n'
                     f'In: {temperature_inside}\u2103')
    lcd.close(clear=True)
