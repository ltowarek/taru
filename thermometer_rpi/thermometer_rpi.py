#!/usr/bin/env python3

import smbus
import bme280
from paho.mqtt.client import Client


MQTT_TEMPERATURE_TOPIC = 'sensor/office/temperature'
MQTT_PRESSURE_TOPIC = 'sensor/office/pressure'
MQTT_HUMIDITY_TOPIC = 'sensor/office/humidity'
MQTT_USERNAME = ''
MQTT_PASSWORD = ''
MQTT_CLIENT = 'sensor/office'
MQTT_SERVER = ''

SENSOR_PORT = 1
SENSOR_ADDRESS = 0x77

if __name__ == '__main__':
    mqtt = Client(client_id=MQTT_CLIENT)
    mqtt.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt.connect(MQTT_SERVER)
    mqtt.loop_start()

    bus = smbus.SMBus(SENSOR_PORT)
    calibration_params = bme280.load_calibration_params(bus, SENSOR_ADDRESS)

    data = bme280.sample(bus, SENSOR_ADDRESS, calibration_params, bme280.oversampling.x16)
    mqtt.publish(MQTT_TEMPERATURE_TOPIC, '{:.2f}'.format(data.temperature))
    mqtt.publish(MQTT_PRESSURE_TOPIC, '{:.2f}'.format(data.pressure * 100))
    mqtt.publish(MQTT_HUMIDITY_TOPIC, '{:.2f}'.format(data.humidity))

    mqtt.loop_stop()
    mqtt.disconnect()
