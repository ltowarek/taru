#!/usr/bin/env python3

import paho.mqtt.client
import serial
import sys


def run():
    fields = [
        'grid_voltage',
        'grid_frequency',
        'ac_output_voltage',
        'ac_output_frequency',
        'ac_output_apparent_power',
        'ac_output_active_power',
        'output_load_percent',
        'bus_voltage',
        'battery_voltage',
        'battery_charging_current',
        'battery_capacity',
        'inverter_heat_sink_temperature',
        'pv_input_current_for_battery',
        'pv_input_voltage',
        'battery_voltage_from_scc',
        'battery_discharge_current'
    ]

    command = bytes.fromhex('51 50 49 47 53 b7 a9 0d') # QPIGS
    with serial.Serial('/dev/serial0', 2400) as s:
        s.timeout = 1
        s.write_timeout = 1
        s.write(command)
        raw_response = s.readline()
        print(raw_response)

    values = raw_response[1:-3].split() # Remove ), <CRC> and <cr>
    response = dict(zip(fields, values))
    print(response)

    client = paho.mqtt.client.Client()
    client.connect('localhost')
    topic_prefix = 'inverter/response/'

    client.loop_start()
    for field, value in response.items():
        topic = topic_prefix + field
        print('Topic: {} Payload: {}'.format(topic, value))
        print(client.publish(topic, value))
    client.loop_stop()

    client.disconnect()
    return 0


if __name__ == '__main__':
    sys.exit(run())

