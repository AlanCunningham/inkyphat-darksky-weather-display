# coding: utf-8
import weather

from inky import InkyPHAT
import buttonshim

import textwrap
import signal
import sys
import ConfigParser
import json
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime


IMAGE_DIR = "climacons"
DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104
WHITE = 0
BLACK = 1
RED = 2


inkyphat = InkyPHAT("black")


def draw_text(base_image, text, x, y, font_size=16):
    font = ImageFont.truetype("fonts/ChiKareGo.ttf", 16)
    draw = ImageDraw.Draw(base_image)
    w, h = font.getsize(text)
    draw.text((x, y), text, inkyphat.BLACK, font)
    inkyphat.set_image(base_image)


def paste_image(base_image, image_to_paste, x, y="middle"):
    image = Image.open(
        "{image_dir}/{image_to_paste}.png".format(
            image_dir=IMAGE_DIR, image_to_paste=image_to_paste
        )
    )
    img_w, img_h = image.size
    if y == "middle":
        y = (inkyphat.HEIGHT - img_h) // 2

    base_image.paste(image, (x, y))
    return base_image


def read_weather_json():
    # weather.json is updated by calling weather.py. This can be done via
    # a cronjob or something similar.
    with open("weather.json") as json_data:
        weather = json.load(json_data)
    return weather


def show_todays_weather():
    forecast = read_weather_json()
    current_weather = forecast["currently"]
    daily_weather = forecast["daily"]["data"][0]
    # Set the data to be drawn on the display
    current_temp = str(int(round(current_weather["apparentTemperature"])))
    high_temp = str(int(round(daily_weather["apparentTemperatureHigh"])))
    low_temp = str(int(round(daily_weather["apparentTemperatureLow"])))

    # Create the base background which we will paste our images to
    base_image = Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    base_image = paste_image(base_image, current_weather["icon"], x=130)
    inkyphat.set_image(base_image)

    draw_text(base_image, current_weather["summary"], x=10, y=20)
    draw_text(base_image, current_temp, x=150, y=80)
    draw_text(base_image, "High: %s" % high_temp, x=10, y=60)
    draw_text(base_image, "Low: %s" % low_temp, x=10, y=80)

    # Draw everything
    inkyphat.show()


def show_daily_weather():
    forecast = read_weather_json()
    weekly_weather = forecast["daily"]["data"]
    today = weekly_weather[0]
    tomorrow = weekly_weather[1]
    overmorrow = weekly_weather[2]

    # Datetime objects
    today_time = datetime.fromtimestamp(today["time"]).strftime("%a")
    tomorrow_time = datetime.fromtimestamp(tomorrow["time"]).strftime("%a")
    overmorrow_time = datetime.fromtimestamp(overmorrow["time"]).strftime("%a")

    base_image = Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    base_image = paste_image(base_image, today["icon"], x=10, y="middle")
    base_image = paste_image(base_image, tomorrow["icon"], x=75, y="middle")
    base_image = paste_image(base_image, overmorrow["icon"], x=140, y="middle")

    inkyphat.set_image(base_image)

    draw_text(base_image, today_time, x=25, y=10)
    draw_text(base_image, tomorrow_time, x=90, y=10)
    draw_text(base_image, overmorrow_time, x=155, y=10)

    today_temp_range = "{low}-{high}".format(
        low=str(int(today["apparentTemperatureLow"])),
        high=str(int(today["apparentTemperatureHigh"])),
    )

    tomorrow_temp_range = "{low}-{high}".format(
        low=str(int(tomorrow["apparentTemperatureLow"])),
        high=str(int(tomorrow["apparentTemperatureHigh"])),
    )

    overmorrow_temp_range = "{low}-{high}".format(
        low=str(int(overmorrow["apparentTemperatureLow"])),
        high=str(int(overmorrow["apparentTemperatureHigh"])),
    )

    draw_text(base_image, today_temp_range, x=25, y=83)
    draw_text(base_image, tomorrow_temp_range, x=90, y=83)
    draw_text(base_image, overmorrow_temp_range, x=155, y=83)

    # Draw everything
    inkyphat.show()


@buttonshim.on_press(buttonshim.BUTTON_A, repeat=False)
def button_todays_weather(button, pressed):
    show_todays_weather()


@buttonshim.on_press(buttonshim.BUTTON_B, repeat=False)
def button_daily_weather(button, pressed):
    show_daily_weather()


# Gracefully stop on Ctrl-C
def signal_handler(signal, frame):
    print("\nGracefully closing, please wait a moment")
    sys.exit(0)


def main():
    # Setup the e-ink display
    print("Setting everything up...")
    inkyphat.set_border(inkyphat.WHITE)

    config = ConfigParser.ConfigParser()
    config.read("config.py")

    weather.get_weather_json()

    # Support for Button SHIM
    if config.getboolean("raspberry_pi", "button_shim"):
        print("Using button shim support")
        show_todays_weather()
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
    else:
        # Show today's weather on the inkyphat
        print("No button shim - showing weather")
        show_todays_weather()


if __name__ == "__main__":
    main()
