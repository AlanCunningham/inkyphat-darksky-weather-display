# Author: Alan Cunningham
# Date 30/05/2016

import requests
import json
from datetime import datetime
import time
import ConfigParser

class Weather:

	result = None

	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.read('config.py')
		url = "https://api.darksky.net/forecast/"
		api_key = config.get('darksky', 'api_key')
		lon = config.get('darksky', 'lon')
		lat = config.get('darksky', 'lat')
		units = config.get('darksky', 'units')

		# Make the initial weather request
		request_url = url + api_key + "/" + lon + "," + lat + "?units=" + units
		r = requests.get(request_url)
		resp = requests.get(url=request_url)
		self.result = json.loads(resp.text)
		self.suggest_clothes()

	def get_current_weather(self):
		current_weather = self.result["currently"]
		return current_weather

	def get_daily_weather(self):
		daily_weather = self.result["daily"]["data"][0]
		return daily_weather

	def get_hourly_weather(self):
		hourly_weather = self.result["hourly"]["data"]
		for keys in hourly_weather:
			keys["time"] = self.convert_epoch(keys["time"])
		return hourly_weather

	def convert_epoch(self, epoch_time):
		converted = datetime.fromtimestamp(epoch_time).strftime('%H:%M')
		return converted

	# Suggest clothes based on the weather.
	def suggest_clothes(self):
		suggestions = []
		daily = self.get_daily_weather()

		# Average weather of the day
		avg_temp = (daily["apparentTemperatureMin"] + daily["apparentTemperatureMax"]) / 2
		rain_chance = daily["precipProbability"]

		# We should extract these out into something configurable
		# Temperature based
		if avg_temp < 11:
			suggestions.append("a coat")
		elif avg_temp >= 10 and avg_temp < 17:
			suggestions.append("a jumper or shirt")
		elif avg_temp >= 17 and avg_temp < 20:
			suggestions.append("a t-shirt")
		else:
			suggestions.append("some shorts")

		# Rain
		if rain_chance > 0.4:
			suggestions.append(". Bring an umbrella")

		suggestion = "Wear " + "".join(suggestions)
		return suggestion

	def set_location(self, long, lat):
		self.location["lon"] = lon
		self.location["lat"] = lat

	def get_location(self):
		return self.location
