#!/usr/bin/env python3

import paho.mqtt.client
from collections import namedtuple
import logging
import serial
import sys


def on_message(client, _, message):
    logging.debug('Payload: {}'.format(message.payload))
    logging.debug('Topic: {}'.format(message.topic))
    qpigs = bytes.fromhex('51 50 49 47 53 b7 a9 0d')
    with serial.Serial('/dev/serial0', 2400) as s:
        s.write(qpigs)

ResponseToken = namedtuple('ResponseToken', ['name', 'start', 'end'])

tokens = [
    ResponseToken('grid_voltage', 1, 6),
    ResponseToken('grid_frequency', 7, 11),
    ResponseToken('ac_output_voltage', 12, 17),
    ResponseToken('ac_output_frequency', 18, 22),
    ResponseToken('ac_output_apparent_power', 23, 27),
    ResponseToken('ac_output_active_power', 28, 32),
    ResponseToken('output_load_percent', 33, 36),
    ResponseToken('bus_voltage', 37, 40),
    ResponseToken('battery_voltage', 41, 46),
    ResponseToken('battery_charging_current', 47, 50),
    ResponseToken('battery_capacity', 51, 54),
    ResponseToken('inverter_heat_sink_temperature', 55, 59),
    ResponseToken('pv_input_current_for_battery', 60, 64),
    ResponseToken('pv_input_voltage', 65, 70),
    ResponseToken('battery_voltage_from_scc', 71, 76),
    ResponseToken('battery_discharge_current', 77, 82),
    ResponseToken('is_sbu_priority_version_added', 83, 84),
    ResponseToken('is_configuration_changed', 84, 85),
    ResponseToken('is_scc_firmware_updated', 85, 86),
    ResponseToken('is_load_on', 86, 87),
    ResponseToken('is_battery_voltage_to_steady_while_charging', 87, 88),
    ResponseToken('is_charging_on', 88, 89),
    ResponseToken('is_scc_charging_on', 89, 90),
    ResponseToken('is_ac_charging_on', 90, 91),
    ResponseToken('battery_voltage_offset_for_fans_on', 92, 94),
    ResponseToken('eeprom_version', 95, 97),
    ResponseToken('pv_charging_power', 98, 103),
    ResponseToken('is_charging_to_floating_enabled', 104, 105),
    ResponseToken('is_switch_on', 105, 106),
    ResponseToken('is_dustproof_installed', 106, 107)
]


def parse_response(raw_response):
    response = {}
    current_byte_id = 0;
    current_token_id = 0;
    current_token_value = ''

    for b in raw_response:
        c = chr(b)
        if c == '(':
            logging.debug('Resetting current byte and token ids')
            current_byte_id = 0
            current_token_id = 0
        else:
            if current_token_id < len(tokens) and current_byte_id == tokens[current_token_id].end:
                logging.debug('Saving response')
                key = tokens[current_token_id].name
                value = current_token_value
                logging.debug('Key: {}'.format(key))
                logging.debug('Value: {}'.format(value))
                response[key] = value
                current_token_id += 1
                logging.debug('Increasing token id to: {}'.format(current_token_id))
            if current_token_id < len(tokens) and current_byte_id == tokens[current_token_id].start:
                logging.debug('Resetting current token value')
                current_token_value = ''
            current_token_value = current_token_value + c
        current_byte_id += 1

    return response


def publish_response(response, client):
    for key, value in response.items():
        logging.debug('Sending response')
        topic = 'inverter/response/' + key
        logging.debug('Topic: {}'.format(topic))
        logging.debug('Payload: {}'.format(value))
        client.publish(topic, value)


def run():
    logging.basicConfig(level=logging.DEBUG)

    client = paho.mqtt.client.Client()
    client.on_message = on_message
    client.connect('localhost')
    client.subscribe('inverter/request')


    try:
        logging.debug('Starting MQTT loop')
        client.loop_start()

        while True:
            with serial.Serial('/dev/serial0', 2400) as s:
                raw_response = s.read_until(b'\r')
                logging.debug('Raw response: {}'.format(raw_response))

                parsed_response = parse_response(raw_response)
                logging.debug('Parsed response: {}'.format(parsed_response))

                publish_response(parsed_response, client)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

    return 0


if __name__ == '__main__':
    sys.exit(run())

