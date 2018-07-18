# Inky pHAT Dark Sky weather display

A Dark Sky weather display for the [Pimoroni Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat).  Displays a short summary of the current weather and temperature, today's highs and lows and uses Dark Sky's [Skycons](https://darkskyapp.github.io/skycons/).

# Dependencies
- [Inky pHAT library](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
- sudo pip install requests

# Setup
Register for a free developer account at https://developer.forecast.io/.  The API offers 1000 requests a day for free, which should be plenty for personal projects like this.
- Update config.py with the following

```
[weather]
api_key: your_dark_sky_api_token
location_lon: your_longitude
location_lat: your_latitude
units: uk2
  ```

# Running everything
From terminal, run `python inky-weather.py`
