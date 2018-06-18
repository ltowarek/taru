#!/usr/bin/env python3

import paho.mqtt.client

class Scheduler():
    def __init__(self):
        self.mqtt_client = None
        
    def initialize(self, host='localhost'):
        self.mqtt_client = paho.mqtt.client.Client()
        self.mqtt_client.connect(host)

    def close(self):
        self.mqtt_client.disconnect()
        
    def send(self, topic, payload):
        self.mqtt_client.publish(topic, payload)

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.initialize()
    scheduler.send('inverter/request', 'QPIGS')
    scheduler.close()

