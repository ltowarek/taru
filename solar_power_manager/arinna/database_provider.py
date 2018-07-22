#!/usr/bin/env python3

import influxdb
import paho.mqtt.client
import logging
import logging.handlers
import sys


logger = logging.getLogger(__name__)


class DatabaseClient:
    def __init__(self):
        self.db_client = None

    def initialize(self, host='localhost'):
        logger.debug('Initializing database client')
        self.db_client = influxdb.InfluxDBClient(host)
        databases = self.db_client.get_list_database()
        database_name = 'inverter'
        if database_name not in [d['name'] for d in databases]:
            logger.debug('Database not found: {}'.format(database_name))
            logger.debug('Creating new database: {}'.format(database_name))
            self.db_client.create_database(database_name)
        self.db_client.switch_database(database_name)
        logger.debug('Database client initialized')

    def close(self):
        logger.debug('Closing database connection')
        self.db_client.close()
        logger.debug('Database connection closed')

    def save(self, measurement, value):
        logger.debug('Saving points into database')
        logger.debug('Measurement: {}'.format(measurement))
        logger.debug('Value: {}'.format(value))
        self.db_client.write_points([{
            'measurement': measurement,
            'fields': {
               'value': value
            }
        }])
        logger.debug('Points saved into database')


def on_message(_, subscriptions, message):
    logger.debug('Message received')
    logger.debug('Payload: {}'.format(message.payload))
    logger.debug('Topic: {}'.format(message.topic))
    db_client = DatabaseClient()
    db_client.initialize()
    topic = message.topic
    subscription = subscriptions[topic]
    raw_value = message.payload.decode().replace(',', '.')
    db_client.save(subscription['measurement'], subscription['type'](raw_value))
    db_client.close()


class MQTTClient:
    def __init__(self):
        self.mqtt_client = None
        self.subscriptions = {}

    def initialize(self, host='localhost'):
        logger.debug('Initializing MQTT client')
        self.mqtt_client = paho.mqtt.client.Client(userdata=self.subscriptions)
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect(host)
        logger.debug('MQTT client initialized')

    def subscribe(self, topic, measurement, type_converter):
        logger.debug('Subscribing to new topic')
        logger.debug('Topic: {}'.format(topic))
        logger.debug('Measurement: {}'.format(measurement))
        logger.debug('Type converter: {}'.format(type_converter))
        self.subscriptions[topic] = {
            'measurement': measurement,
            'type': type_converter
        }
        self.mqtt_client.subscribe(topic)
        logger.debug('Subscribed to new topic')

    def close(self):
        logger.debug('Disconnecting MQTT client')
        self.mqtt_client.disconnect()
        logger.debug('MQTT client disconnected')

    def loop(self):
        logger.debug('MQTT client loop')
        self.mqtt_client.loop()


def setup_logging():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.TimedRotatingFileHandler('database_provider.log', interval=5, when='m')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def percent(value):
    return float(int(value)/100)


def run():
    setup_logging()

    mqtt_client = MQTTClient()
    mqtt_client.initialize()

    mqtt_client.subscribe('inverter/response/grid_voltage', 'grid_voltage', float)
    mqtt_client.subscribe('inverter/response/grid_frequency', 'grid_frequency', float)
    mqtt_client.subscribe('inverter/response/ac_output_voltage', 'ac_output_voltage', float)
    mqtt_client.subscribe('inverter/response/ac_output_frequency', 'ac_output_frequency', float)
    mqtt_client.subscribe('inverter/response/ac_output_apparent_power', 'ac_output_apparent_power', int)
    mqtt_client.subscribe('inverter/response/ac_output_active_power', 'ac_output_active_power', int)
    mqtt_client.subscribe('inverter/response/output_load_percent', 'output_load_percent', percent)
    mqtt_client.subscribe('inverter/response/bus_voltage', 'bus_voltage', int)
    mqtt_client.subscribe('inverter/response/battery_voltage', 'battery_voltage', float)
    mqtt_client.subscribe('inverter/response/battery_charging_current', 'battery_charging_current', int)
    mqtt_client.subscribe('inverter/response/battery_capacity', 'battery_capacity', percent)
    mqtt_client.subscribe('inverter/response/inverter_heat_sink_temperature', 'inverter_heat_sink_temperature', int)
    mqtt_client.subscribe('inverter/response/pv_input_current_for_battery', 'pv_input_current_for_battery', int)
    mqtt_client.subscribe('inverter/response/pv_input_voltage', 'pv_input_voltage', float)
    mqtt_client.subscribe('inverter/response/battery_voltage_from_scc', 'battery_voltage_from_scc', float)
    mqtt_client.subscribe('inverter/response/battery_discharge_current', 'battery_discharge_current', int)
    mqtt_client.subscribe('inverter/response/is_sbu_priority_version_added', 'is_sbu_priority_version_added', bool)
    mqtt_client.subscribe('inverter/response/is_sbu_priority_version_added', 'is_sbu_priority_version_added', bool)
    mqtt_client.subscribe('inverter/response/is_configuration_changed', 'is_configuration_changed', bool)
    mqtt_client.subscribe('inverter/response/is_scc_firmware_updated', 'is_scc_firmware_updated', bool)
    mqtt_client.subscribe('inverter/response/is_load_on', 'is_load_on', bool)
    mqtt_client.subscribe('inverter/response/is_battery_voltage_to_steady_while_charging', 'is_battery_voltage_to_steady_while_charging', bool)
    mqtt_client.subscribe('inverter/response/is_charging_on', 'is_charging_on', bool)
    mqtt_client.subscribe('inverter/response/is_scc_charging_on', 'is_scc_charging_on', bool)
    mqtt_client.subscribe('inverter/response/is_ac_charging_on', 'is_ac_charging_on', bool)
    mqtt_client.subscribe('inverter/response/battery_voltage_offset_for_fans_on', 'battery_voltage_offset_for_fans_on', int)
    mqtt_client.subscribe('inverter/response/eeprom_version', 'eeprom_version', int)
    mqtt_client.subscribe('inverter/response/pv_charging_power', 'pv_charging_power', int)
    mqtt_client.subscribe('inverter/response/is_charging_to_floating_enabled', 'is_charging_to_floating_enabled', bool)
    mqtt_client.subscribe('inverter/response/is_switch_on', 'is_switch_on', bool)
    mqtt_client.subscribe('inverter/response/is_dustproof_installed', 'is_dustproof_installed', bool)

    logger.debug('MQTT loop started')
    try:
        while True:
            mqtt_client.loop()
    except KeyboardInterrupt:
        logger.debug('MQTT loop stopped by user')
    except Exception as e:
        logger.exception('Unknown exception occurred', e)
    finally:
        mqtt_client.close()
    logger.debug('MQTT loop stopped')

    return 0


if __name__ == '__main__':
    sys.exit(run())
