#!/usr/bin/env python
import os

import smbus2, bme280
from influxdb import InfluxDBClient

INFLUX_URL = os.environ.get('INFLUX_URL')
INFLUX_PORT = os.environ.get('INFLUX_PORT')
INFLUX_USERNAME = os.environ.get('INFLUX_USERNAME')
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD')
INFLUX_DATABASE = os.environ.get('INFLUX_DATABASE')

MINUTES_BETWEEN_READS = 3

# Influx
try:
    client = InfluxDBClient(host=INFLUX_URL, port=INFLUX_PORT, username=INFLUX_USERNAME, password=INFLUX_PASSWORD)
    client.switch_database(INFLUX_DATABASE)
except Exception:
    raise

# BME280 settings 
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

bme280data = bme280.sample(bus, address, calibration_params)
humidity = bme280data.humidity
pressure = bme280data.pressure
temp_c = bme280data.temperature

json_body = [ 
  {
    "measurement": "environment_data",
    "tags": {
        "source": "basement_1",
    },
    "fields": {
        "temperature": float(temp_c),
        "humidity": float(humidity),
        "pressure": float(pressure)
    }
  }
]

client.write_points(json_body)
