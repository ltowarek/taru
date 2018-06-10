#!/usr/bin/env python3

import unittest
import influxdb

class DatabaseLinkTest(unittest.TestCase):
    def test_database_link_does_inverter_database_exist(self):
        client = influxdb.InfluxDBClient()
        self.assertIn({'name': 'inverter'}, client.get_list_database())
        client.close()


if __name__ == '__main__':
    unittest.main()


