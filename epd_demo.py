#!/usr/bin/env python3
import time
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

try:
    from waveshare_epd import epd2in13b_V4
except ImportError:
    import sys
    sys.path.append("/home/pi/e-Paper/RaspberryPi_Jetson/python/lib")
    from waveshare_epd import epd2in13b_V4


def main():
    GPIO.setmode(GPIO.BCM)
    try:
        epd = epd2in13b_V4.EPD()
        epd.init()
        epd.Clear()

        width = epd.height   # 250
        height = epd.width   # 122

        bw = Image.new('1', (width, height), 255)
        red = Image.new('1', (width, height), 255)
        d = ImageDraw.Draw(bw)

        # Load fonts
        try:
            font_big = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Title
        d.text((4, 4), "E-Ink Demo OK", font=font_big, fill=0)

        # Fake song line
        d.text((4, 26), "Song: Test Track", font=font_small, fill=0)

        # Progress bar background
        bar_x = 4
        bar_y = 46
        bar_w = width - 30
        bar_h = 10
        d.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), outline=0, width=1)

        # 40% filled
        fill_w = int(bar_w * 0.4)
        d.rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h), fill=0)

        # Time display
        d.text((4, bar_y + bar_h + 4), "01:23 / 03:45", font=font_small, fill=0)

        # BT status
        d.text((4, 80), "BT: Not Connected", font=font_small, fill=0)

        # Volume bar
        max_steps = 10
        vol = 6
        vol_x = width - 12
        vol_top = 10
        vol_bottom = height - 10

        step_h = (vol_bottom - vol_top) / max_steps
        d.line((vol_x, vol_top, vol_x, vol_bottom), fill=0, width=1)

        for i in range(max_steps):
            y = vol_bottom - (i + 0.5) * step_h
            rect = (vol_x - 3, y - 2, vol_x + 3, y + 2)
            if i < vol:
                d.rectangle(rect, fill=0)
            else:
                d.rectangle(rect, outline=0)

        d.text((4, height - 14), "RPi OS Demo", font=font_small, fill=0)

        epd.display(epd.getbuffer(bw), epd.getbuffer(red))

        time.sleep(10)
        epd.sleep()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
