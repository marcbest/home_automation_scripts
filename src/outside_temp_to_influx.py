#!/usr/bin/env python3
import requests, json, os 
from influxdb import InfluxDBClient

OPEN_WEATHER_API_KEY=''
OPEN_WEATHER_CITY_NAME=''
BASE_URL = ''
INFLUX_URL=''
INFLUX_USERNAME=''
INFLUX_PASSWORD=''
INFLUX_DATABASE=''

client = InfluxDBClient(host=INFLUX_URL, port=8086, username=INFLUX_USERNAME, password=INFLUX_PASSWORD)
client.switch_database(INFLUX_DATABASE)

complete_url = BASE_URL + "appid=" + OPEN_WEATHER_API_KEY + "&q=" + OPEN_WEATHER_CITY_NAME + "&units=metric"

response = requests.get(complete_url).json()

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
