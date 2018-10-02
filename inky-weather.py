# coding: utf-8
import inkyphat
import weather

import textwrap
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
    show_todays_weather(forecast)


def show_todays_weather(weather):
    current_weather = weather.get_current_weather()
    daily_weather = weather.get_daily_weather()
    # Create the base background which we will paste our images to
    base_image = inkyphat.Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    image_to_paste = Image.open(
        "{image_dir}/{image_to_paste}.png".format(
            image_dir=IMAGE_DIR, image_to_paste=current_weather["icon"]
        )
    )
    img_w, img_h = image_to_paste.size
    vertical_align = (inkyphat.HEIGHT - img_h) // 2
    base_image = paste_image(
        base_image, current_weather["icon"], x=130, y=vertical_align
    )
    inkyphat.paste(base_image)

    # Set the data to be drawn on the display
    current_temp = str(int(round(current_weather["apparentTemperature"])))
    high_temp = str(int(round(daily_weather["apparentTemperatureHigh"])))
    low_temp = str(int(round(daily_weather["apparentTemperatureLow"])))
    draw_text(current_weather["summary"], x=10, y=20, font_size=16)
    draw_text(current_temp, x=150, y=80, font_size=16)
    draw_text("High: %s" % high_temp, x=10, y=60, font_size=16)
    draw_text("Low: %s" % low_temp, x=10, y=80, font_size=16)

    # Draw everything
    inkyphat.show()


def draw_text(text, x, y, font_size):
    font = ImageFont.truetype("fonts/ChiKareGo.ttf", font_size)
    w, h = font.getsize(text)
    inkyphat.text((x, y), text, inkyphat.BLACK, font)


def draw_image(image):
    inkyphat.set_image(
        Image.open("{image_dir}/{image}.png".format(image_dir=IMAGE_DIR, image=image))
    )


def paste_image(base_image, image_to_paste, x, y):
    image = Image.open(
        "{image_dir}/{image_to_paste}.png".format(
            image_dir=IMAGE_DIR, image_to_paste=image_to_paste
        )
    )
    base_image.paste(image, (x, y))
    return base_image


if __name__ == "__main__":
    init()
