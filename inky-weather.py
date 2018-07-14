# coding: utf-8

import inkyphat
import weather
from PIL import ImageFont, Image

from datetime import datetime
import ConfigParser
import textwrap

image_path = 'images/'


def init():
    # Setup the e-ink display
    inkyphat.set_colour('black')
    inkyphat.set_rotation(180)
    inkyphat.set_border(inkyphat.WHITE)

    # Get the current weather
    forecast = weather.Weather()
    current_weather = forecast.get_current_weather()
    daily_weather = forecast.get_daily_weather()

    weather_info = {
        'summary': current_weather['summary'],
        'current_temp': str(int(round(current_weather['apparentTemperature']))),
        'high_temp': str(int(round(daily_weather['apparentTemperatureHigh']))),
        'low_temp': str(int(round(daily_weather['apparentTemperatureLow']))),
        'icon': current_weather['icon'],
    }

    print(weather_info)

    draw_image(weather_info['icon'])

    # Set the data to be drawn on the display
    draw_text(weather_info['summary'], x=10, y=10, font_size=32)
    draw_text(weather_info['current_temp'], x=154, y=70, font_size=16)
    draw_text('High: %s' % weather_info['high_temp'], x=10, y=50, font_size=16)
    draw_text('Low: %s' % weather_info['low_temp'], x=10, y=70, font_size=16)

    # draw_image(weather_info['icon'])
    # draw_image('1-clear-day')
    # Draw everything
    inkyphat.show()


def draw_text(text, x, y, font_size):
    font = ImageFont.truetype('fonts/ChiKareGo.ttf', font_size)
    w, h = font.getsize(text)
    inkyphat.text((x, y), text, inkyphat.BLACK, font)


def draw_image(image):
    inkyphat.set_image(Image.open(image_path + image + '.png'))


if __name__ == '__main__':
    init()
