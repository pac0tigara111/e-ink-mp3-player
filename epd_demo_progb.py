#!/usr/bin/env python3
import time
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

from waveshare_epd import epd2in13b_V4


def main():
    GPIO.setmode(GPIO.BCM)
    try:
        epd = epd2in13b_V4.EPD()
        epd.init()   # no Clear() to save one extra flash

        width = epd.height   # 250
        height = epd.width   # 122

        # Base image (static UI)
        base_bw = Image.new('1', (width, height), 255)  # white
        red = Image.new('1', (width, height), 255)
        d = ImageDraw.Draw(base_bw)

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

        # --- Static parts of UI ---
        d.text((4, 4), "Progress demo", font=font_big, fill=0)
        d.text((4, 24), "Bar fills in 10 seconds", font=font_small, fill=0)

        # Progress bar geometry
        bar_x = 4
        bar_y = 48
        bar_w = width - 30
        bar_h = 10

        # Draw bar outline once on base image
        d.rectangle(
            (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
            outline=0,
            width=1
        )

        d.text((4, bar_y + bar_h + 4), "Animating...", font=font_small, fill=0)

        # Volume bar static example (just for looks)
        max_steps = 10
        current_vol = 6
        vol_x = width - 12
        vol_top = 10
        vol_bottom = height - 10

        d.line((vol_x, vol_top, vol_x, vol_bottom), fill=0, width=1)
        step_h = (vol_bottom - vol_top) / max_steps
        for i in range(max_steps):
            y = vol_bottom - (i + 0.5) * step_h
            rect = (vol_x - 3, y - 2, vol_x + 3, y + 2)
            if i < current_vol:
                d.rectangle(rect, fill=0)
            else:
                d.rectangle(rect, outline=0)

        # Initial draw (empty bar)
        frame = base_bw.copy()
        epd.display(epd.getbuffer(frame), epd.getbuffer(red))

        # --- Animate progress bar over ~10 seconds ---
        STEPS = 20          # number of updates (20 = every 0.5s)
        TOTAL_TIME = 10.0   # seconds
        STEP_DELAY = TOTAL_TIME / STEPS

        for i in range(1, STEPS + 1):
            frac = i / STEPS  # 0.0 -> 1.0

            # Start from base (no fill), then draw new fill
            frame = base_bw.copy()
            df = ImageDraw.Draw(frame)

            fill_w = int(bar_w * frac)
            df.rectangle(
                (bar_x, bar_y, bar_x + fill_w, bar_y + bar_h),
                fill=0
            )

            # Optional: show percentage text
            percent_text = f"{int(frac * 100)}%"
            df.text(
                (bar_x + bar_w + 2, bar_y - 2),
                percent_text,
                font=font_small,
                fill=0
            )

            epd.display(epd.getbuffer(frame), epd.getbuffer(red))
            time.sleep(STEP_DELAY)

        # After animation, show "Done"
        frame = base_bw.copy()
        df = ImageDraw.Draw(frame)
        df.rectangle(
            (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
            fill=0
        )
        df.text((4, height - 14), "Done!", font=font_small, fill=0)

        epd.display(epd.getbuffer(frame), epd.getbuffer(red))

        time.sleep(3)
        epd.sleep()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
