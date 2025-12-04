#!/usr/bin/env python3
import time
from PIL import Image, ImageDraw, ImageFont

import RPi.GPIO as GPIO

try:
    from waveshare_epd import epd2in13b_V4
except ImportError:
    # Adjust path if needed depending on where you cloned the repo
    import sys
    sys.path.append("/home/dietpi/e-Paper/RaspberryPi_Jetson/python/lib")
    from waveshare_epd import epd2in13b_V4


def main():
    GPIO.setmode(GPIO.BCM)
    try:
        epd = epd2in13b_V4.EPD()
        epd.init()
        epd.Clear()

        # On this display epd.width/height are usually 122x250 or 250x122
        # We'll treat it as "vertical": 250 (long side) x 122 (short side)
        width = epd.height   # 250
        height = epd.width   # 122

        # Create black/white and red images
        bw = Image.new('1', (width, height), 255)  # 255 = white
        red = Image.new('1', (width, height), 255)

        draw_bw = ImageDraw.Draw(bw)

        # Load fonts
        try:
            font_big = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
            )
            font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
            )
        except Exception:
            # Fallback to default if truetype not found
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # ------------------------------
        # Fake UI like your MP3 player
        # ------------------------------

        # Title at top
        title = "Demo: E-ink OK"
        draw_bw.text((4, 4), title, font=font_big, fill=0)

        # Fake song name
        song = "Song: Test Track 01"
        draw_bw.text((4, 26), song, font=font_small, fill=0)

        # Progress bar
        bar_x = 4
        bar_y = 46
        bar_w = width - 30
        bar_h = 10

        draw_bw.rectangle(
            (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
            outline=0,
            width=1,
        )

        # Fill ~40% progress
        progress_fraction = 0.4
        fill_w = int(bar_w * progress_fraction)
        draw_bw.rectangle(
            (bar_x, bar_y, bar_x + fill_w, bar_y + bar_h),
            fill=0,
        )

        # Time text under progress bar
        time_text = "01:23 / 03:45"
        draw_bw.text((4, bar_y + bar_h + 4), time_text, font=font_small, fill=0)

        # Bluetooth status line
        bt_text = "BT: Not connected (demo)"
        draw_bw.text((4, 80), bt_text, font=font_small, fill=0)

        # Volume bar (10 steps) on the right side
        max_steps = 10
        current_vol = 6  # just some demo volume level

        vol_x = width - 12
        vol_y_top = 10
        vol_y_bottom = height - 10

        # Draw vertical line
        draw_bw.line(
            (vol_x, vol_y_top, vol_x, vol_y_bottom),
            fill=0,
            width=1,
        )

        step_h = (vol_y_bottom - vol_y_top) / max_steps
        for i in range(max_steps):
            y = vol_y_bottom - (i + 0.5) * step_h
            rect = (vol_x - 3, y - 2, vol_x + 3, y + 2)
            if i < current_vol:
                draw_bw.rectangle(rect, fill=0)
            else:
                draw_bw.rectangle(rect, outline=0)

        # Footer
        footer = "DietPi display demo"
        draw_bw.text((4, height - 14), footer, font=font_small, fill=0)

        # Send to display
        epd.display(epd.getbuffer(bw), epd.getbuffer(red))

        print("Demo shown. Sleeping 10 seconds...")
        time.sleep(10)

        # Optional: clear or sleep
        # epd.Clear()
        epd.sleep()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
