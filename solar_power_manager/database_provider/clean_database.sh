#!/bin/sh
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DROP DATABASE inverter"
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE inverter"

