# Author: Alan Cunningham
# Date 30/05/2016

import requests
import json
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

def get_weather_json():
	config = configparser.ConfigParser()
	config.read('config.py')
	url = "https://api.darksky.net/forecast/"
	api_key = config.get('darksky', 'api_key')
	lon = config.get('darksky', 'lon')
	lat = config.get('darksky', 'lat')
	units = config.get('darksky', 'units')

	# Make the weather request and save to a json file
	request_url = url + api_key + "/" + lon + "," + lat + "?units=" + units
	resp = requests.get(url=request_url)
	result = json.loads(resp.text)
	print("Retrieved weather for {country}".format(country=result["timezone"]))
	with open("weather.json", "w") as outfile:
		json.dump(result, outfile)

if __name__ == "__main__":
	get_weather_json()