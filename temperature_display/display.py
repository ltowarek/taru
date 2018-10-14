#!/usr/bin/env python3

from RPLCD.i2c import CharLCD
from paho.mqtt.client import Client


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


MQTT_OUTSIDE_TEMPERATURE_TOPIC = 'sensor/balcony/temperature'
MQTT_INSIDE_TEMPERATURE_TOPIC = 'sensor/office/temperature'
MQTT_USERNAME = ''
MQTT_PASSWORD = ''
MQTT_CLIENT = 'display'
MQTT_SERVER = ''


def on_message(_, lcd, message):
    topic = message.topic
    value = float(message.payload)
    if topic == MQTT_OUTSIDE_TEMPERATURE_TOPIC:
        lcd.print_outside_temperature(value)
    elif topic == MQTT_INSIDE_TEMPERATURE_TOPIC:
        lcd.print_inside_temperature(value)


if __name__ == '__main__':
    mqtt = Client(client_id=MQTT_CLIENT)
    mqtt.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt.connect(MQTT_SERVER)
    mqtt.on_message = on_message
    mqtt.subscribe(MQTT_OUTSIDE_TEMPERATURE_TOPIC)
    mqtt.subscribe(MQTT_INSIDE_TEMPERATURE_TOPIC)
    with LCD() as lcd:
        mqtt.user_data_set(lcd)
        mqtt.loop_forever()
