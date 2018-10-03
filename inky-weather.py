# coding: utf-8
import inkyphat
import weather

import textwrap
from datetime import datetime
from PIL import ImageFont, Image
from datetime import datetime


IMAGE_DIR = "climacons"
DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104
WHITE = 0
BLACK = 1
RED = 2


def init():
    # Setup the e-ink display
    inkyphat.set_colour("black")
    inkyphat.set_rotation(180)
    inkyphat.set_border(inkyphat.WHITE)

    # Show today's weather on the inkyphat
    forecast = weather.Weather()
    # show_todays_weather(forecast)
    show_daily_weather(forecast)


def draw_text(text, x, y, font_size=16):
    font = ImageFont.truetype("fonts/ChiKareGo.ttf", font_size)
    w, h = font.getsize(text)
    inkyphat.text((x, y), text, inkyphat.BLACK, font)


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


def show_todays_weather(weather):
    current_weather = weather.get_current_weather()
    daily_weather = weather.get_daily_weather()[0]
    # Set the data to be drawn on the display
    current_temp = str(int(round(current_weather["apparentTemperature"])))
    high_temp = str(int(round(daily_weather["apparentTemperatureHigh"])))
    low_temp = str(int(round(daily_weather["apparentTemperatureLow"])))

    # Create the base background which we will paste our images to
    base_image = inkyphat.Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    base_image = paste_image(base_image, current_weather["icon"], x=130)
    inkyphat.paste(base_image)

    draw_text(current_weather["summary"], x=10, y=20)
    draw_text(current_temp, x=150, y=80)
    draw_text("High: %s" % high_temp, x=10, y=60)
    draw_text("Low: %s" % low_temp, x=10, y=80)

    # Draw everything
    inkyphat.show()


def show_daily_weather(weather):
    weekly_weather = weather.get_daily_weather()
    today = weekly_weather[1]
    tomorrow = weekly_weather[2]
    overmorrow = weekly_weather[3]

    # Datetime objects
    today_time = datetime.fromtimestamp(today["time"]).strftime("%a")
    tomorrow_time = datetime.fromtimestamp(tomorrow["time"]).strftime("%a")
    overmorrow_time = datetime.fromtimestamp(overmorrow["time"]).strftime("%a")

    base_image = inkyphat.Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    base_image = paste_image(base_image, today["icon"], x=10, y=30)
    base_image = paste_image(base_image, tomorrow["icon"], x=75, y=30)
    base_image = paste_image(base_image, overmorrow["icon"], x=140, y=30)
    inkyphat.paste(base_image)

    draw_text(today_time, x=25, y=10, font_size=16)
    draw_text(tomorrow_time, x=90, y=10, font_size=16)
    draw_text(overmorrow_time, x=155, y=10, font_size=16)

    today_avg_temp = "{low}-{high}".format(
        low=str(int(today["apparentTemperatureLow"])),
        high=str(int(today["apparentTemperatureHigh"])),
    )

    tomorrow_avg_temp = "{low}-{high}".format(
        low=str(int(tomorrow["apparentTemperatureLow"])),
        high=str(int(tomorrow["apparentTemperatureHigh"])),
    )

    overmorrow_avg_temp = "{low}-{high}".format(
        low=str(int(overmorrow["apparentTemperatureLow"])),
        high=str(int(overmorrow["apparentTemperatureHigh"])),
    )

    draw_text(today_avg_temp, x=25, y=83, font_size=16)
    draw_text(tomorrow_avg_temp, x=90, y=83, font_size=16)
    draw_text(overmorrow_avg_temp, x=155, y=83, font_size=16)

    # Draw everything
    inkyphat.show()


if __name__ == "__main__":
    init()
