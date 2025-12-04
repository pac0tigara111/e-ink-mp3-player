#!/usr/bin/env python3
import time
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

from waveshare_epd import epd2in13b_V4


def main():
    GPIO.setmode(GPIO.BCM)
    try:
        epd = epd2in13b_V4.EPD()
        epd.init()   # no Clear() here – faster

        width = epd.height   # 250 (long side)
        height = epd.width   # 122 (short side)

        # Simple black/white buffer
        bw = Image.new('1', (width, height), 255)  # white
        red = Image.new('1', (width, height), 255)
        d = ImageDraw.Draw(bw)

        # Fonts
        try:
            font_big = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
            )
            font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
            )
        except Exception:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # VERY SIMPLE UI to keep refresh light
        d.text((4, 4), "Fast demo", font=font_big, fill=0)
        d.text((4, 26), "E-ink initialized", font=font_small, fill=0)

        # Tiny progress bar (short)
        bar_x = 4
        bar_y = 46
        bar_w = width - 40
        bar_h = 8
        d.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
                    outline=0, width=1)
        fill_w = int(bar_w * 0.6)
        d.rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h),
                    fill=0)

        d.text((4, height - 14), "Fast load test", font=font_small, fill=0)

        # Single refresh
        epd.display(epd.getbuffer(bw), epd.getbuffer(red))

        # Short wait just so you can see it before script exits
        time.sleep(3)
        epd.sleep()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
