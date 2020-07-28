#!/usr/bin/env python3
import os
import requests
from influxdb import InfluxDBClient

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
OPEN_WEATHER_CITY_NAME = os.environ.get('OPEN_WEATHER_CITY_NAME')
BASE_URL = os.environ.get('BASE_URL')
INFLUX_URL = os.environ.get('INFLUX_URL')
INFLUX_PORT = os.environ.get('INFLUX_PORT')
INFLUX_USERNAME = os.environ.get('INFLUX_USERNAME')
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD')
INFLUX_DATABASE = os.environ.get('INFLUX_DATABASE')

try:
	client = InfluxDBClient(host=INFLUX_URL, port=INFLUX_PORT, username=INFLUX_USERNAME, password=INFLUX_PASSWORD)
	client.switch_database(INFLUX_DATABASE)
except Exception:
	raise

params = {
	'appid': OPEN_WEATHER_API_KEY,
	'q': OPEN_WEATHER_CITY_NAME,
	'units': 'metric'
}
response = requests.get(BASE_URL, params=params).json()

if response["cod"] == 200:
	data = response["main"]

	current_temperature = data["temp"]
	current_pressure = data["pressure"]
	current_humidity = data["humidity"]

	weather = response["weather"]

	weather_description = weather[0]["description"]
	json_body = [
		{
			"measurement": "environment_data",
			"tags": {
				"source": "openweathermap",
			},
			"fields": {
				"temperature": float(current_temperature),
				"pressure": float(current_pressure),
				"humidity": float(current_humidity),
				"weather_description": weather_description
			}
		}
	]

	client.write_points(json_body)
else:
	print("Failed")
