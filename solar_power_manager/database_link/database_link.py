#!/usr/bin/env python3

import influxdb

if __name__ == '__main__':
    client = influxdb.InfluxDBClient()
    databases = client.get_list_database()
    database_name = 'inverter'
    if database_name not in databases:
        client.create_database(database_name)
    client.switch_database(database_name)
    client.close()

