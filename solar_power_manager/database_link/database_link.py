#!/usr/bin/env python3

import influxdb
import paho.mqtt.client
import logging
import os

def on_message(client, database_link, message):
    logging.debug('Payload: {}'.format(message.payload))
    logging.debug('Topic: {}'.format(message.topic))
    database_link.save(message.topic, message.payload.decode())

class DatabaseLink():
    def __init__(self):
        self.db_client = None
        self.mqtt_client = None
        self.subscriptions = {}
        
    def initialize(self, host='localhost'):
        self.db_client = influxdb.InfluxDBClient(host)

        databases = self.db_client.get_list_database()
        database_name = 'inverter'
        if database_name not in [d['name'] for d in databases]:
            self.db_client.create_database(database_name)
        self.db_client.switch_database(database_name)

        self.mqtt_client = paho.mqtt.client.Client(userdata=self)
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect(host)

    def subscribe(self, topic, measurement, type_converter):
        self.subscriptions[topic] = {
            'measurement': measurement,
            'type': type_converter
        }
        self.mqtt_client.subscribe(topic)
        
    def close(self):
        self.db_client.close()
        self.mqtt_client.disconnect()
        
    def loop(self):
        self.mqtt_client.loop()

    def loop_start(self):
        self.mqtt_client.loop_start()

    def loop_stop(self):
        self.mqtt_client.loop_stop()

    def save(self, topic, raw_value):
        s = self.subscriptions[topic]
        self.db_client.write_points([{
            'measurement': s['measurement'],
            'fields': {
                'value': s['type'](raw_value)
             }
        }])


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

