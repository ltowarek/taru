#!/usr/bin/env python3

import influxdb
import paho.mqtt.client
import logging
import os
import sys

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


def percent(value):
    return float(int(value)/100)


def run():
    logging.basicConfig(level=logging.DEBUG)
    link = DatabaseLink()
    link.initialize()

    link.subscribe('inverter/response/grid_voltage', 'grid_voltage', int)
    link.subscribe('inverter/response/grid_frequency', 'grid_frequency', int)
    link.subscribe('inverter/response/grid_frequency', 'grid_frequency', int)
    link.subscribe('inverter/response/ac_output_voltage', 'ac_output_voltage', int)
    link.subscribe('inverter/response/ac_output_apparent_power', 'ac_output_apparent_power', int)
    link.subscribe('inverter/response/ac_output_active_power', 'ac_output_active_power', int)
    link.subscribe('inverter/response/output_load_percent', 'output_load_percent', percent)
    link.subscribe('inverter/response/ac_output_voltage', 'ac_output_voltage', int)
    link.subscribe('inverter/response/bus_voltage', 'bus_voltage', int)
    link.subscribe('inverter/response/battery_voltage', 'battery_voltage', int)
    link.subscribe('inverter/response/battery_charging_current', 'battery_charging_current', int)
    link.subscribe('inverter/response/battery_capacity', 'battery_capacity', int)
    link.subscribe('inverter/response/inverter_heat_sink_temperature', 'inverter_heat_sink_temperature', int)
    link.subscribe('inverter/response/pv_input_current_for_battery', 'pv_input_current_for_battery', int)
    link.subscribe('inverter/response/pv_input_voltage', 'pv_input_voltage', int)
    link.subscribe('inverter/response/battery_voltage_from_scc', 'battery_voltage_from_scc', int)
    link.subscribe('inverter/response/battery_discharge_current', 'battery_discharge_current', int)
    link.subscribe('inverter/response/is_sbu_priority_version_added', 'is_sbu_priority_version_added', bool)
    link.subscribe('inverter/response/is_sbu_priority_version_added', 'is_sbu_priority_version_added', bool)
    link.subscribe('inverter/response/is_configuration_changed', 'is_configuration_changed', bool)
    link.subscribe('inverter/response/is_scc_firmware_updated', 'is_scc_firmware_updated', bool)
    link.subscribe('inverter/response/is_load_on', 'is_load_on', bool)
    link.subscribe('inverter/response/is_battery_voltage_to_steady_while_charging', 'is_battery_voltage_to_steady_while_charging', bool)
    link.subscribe('inverter/response/is_charging_on', 'is_charging_on', bool)
    link.subscribe('inverter/response/is_scc_charging_on', 'is_scc_charging_on', bool)
    link.subscribe('inverter/response/is_ac_charging_on', 'is_ac_charging_on', bool)
    link.subscribe('inverter/response/battery_voltage_offset_for_fans_on', 'battery_voltage_offset_for_fans_on', int)
    link.subscribe('inverter/response/eeprom_version', 'eeprom_version', int)
    link.subscribe('inverter/response/pv_charging_power', 'pv_charging_power', int)
    link.subscribe('inverter/response/is_charging_to_floating_enabled', 'is_charging_to_floating_enabled', bool)
    link.subscribe('inverter/response/is_switch_on', 'is_switch_on', bool)
    link.subscribe('inverter/response/is_dustproof_installed', 'is_dustproof_installed', bool)

    try:
        while True:
            link.loop()
    except KeyboardInterrupt:
        link.loop_stop()
        link.close()

    return 0

if __name__ == '__main__':
    sys.exit(run())

