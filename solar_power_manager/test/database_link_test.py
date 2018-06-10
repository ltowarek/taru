#!/usr/bin/env python3

import unittest
import database_link.database_link as db_link
import paho.mqtt.client as mqtt
import influxdb
import time

class DatabaseLinkTest(unittest.TestCase):
    def test_database_link_writes_points_from_mqtt_message(self):
        measurement = 'test_measurement'
        value = 123
        topic = 'inverter/{}'.format(measurement)
        db_name = '"inverter"."autogen"."{}"'.format(measurement)

        db_client = influxdb.InfluxDBClient()
        db_client.switch_database('inverter')
        db_client.drop_measurement(measurement)

        link = db_link.DatabaseLink()
        link.initialize()
        link.loop_start()

        mqtt_client = mqtt.Client()
        mqtt_client.connect('localhost')
        mqtt_client.publish(topic, value)
        mqtt_client.disconnect()

        time.sleep(1)
        
        results = db_client.query('SELECT value FROM {}'.format(db_name))
        points = results.get_points()
        self.assertIn(value, [p['value'] for p in points])

        link.loop_stop()
        link.close()
        db_client.close()


if __name__ == '__main__':
    unittest.main()


