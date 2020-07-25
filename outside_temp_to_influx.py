#!/usr/bin/env python3
import requests, json, os 
from influxdb import InfluxDBClient

API_KEY='a301dc655425b65ce89ae14cc64cf915'
CITY_NAME='Hemel Hempstead'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
INFLUX_URL=''
INFLUX_USERNAME=''
INFLUX_PASSWORD=''
INFLUX_DATABASE=''

client = InfluxDBClient(host=INFLUX_URL, port=8086, username=INFLUX_USERNAME, password=INFLUX_PASSWORD)
client.switch_database('INFLUX_DATABASE')

complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY_NAME + "&units=metric"

response = requests.get(complete_url).json()

if response["cod"] != "404": 
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
