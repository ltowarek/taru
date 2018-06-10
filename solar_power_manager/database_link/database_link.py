#!/usr/bin/env python3

import influxdb
import paho.mqtt.client as mqtt
import logging
import os

def on_message(client, user_data, message):
    logging.debug('Payload: {}'.format(message.payload))
    logging.debug('Topic: {}'.format(message.topic))
    user_data.save(os.path.basename(message.topic), int(message.payload))

class DatabaseLink():
    def __init__(self):
        self.db_client = None
        self.mqtt_client = None
        
    def initialize(self, host='localhost'):
        self.db_client = influxdb.InfluxDBClient(host)

        databases = self.db_client.get_list_database()
        database_name = 'inverter'
        if database_name not in [d['name'] for d in databases]:
            self.db_client.create_database(database_name)
        self.db_client.switch_database(database_name)

        self.mqtt_client = mqtt.Client(userdata=self)
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect(host)
        self.mqtt_client.subscribe('inverter/test_measurement')
        
    def close(self):
        self.db_client.close()
        self.mqtt_client.disconnect()
        
    def loop(self):
        self.mqtt_client.loop()

    def loop_start(self):
        self.mqtt_client.loop_start()

    def loop_stop(self):
        self.mqtt_client.loop_stop()

    def save(self, measurement, value):
        self.db_client.write_points([{'measurement': measurement, 'fields': {'value': value}}])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    link = DatabaseLink()
    link.initialize()
    try:
        while True:
            link.loop()
    except KeyboardInterrupt:
        link.loop_stop()
        link.close()

