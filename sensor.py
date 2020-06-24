"""
Dependencies:
* nodemcu_gpio_lcd.py and lcd_api.py from https://github.com/dhylands/python_lcd
"""

from machine import Pin, UART
from utime import sleep, ticks_ms
from nodemcu_gpio_lcd import GpioLcd

import uos
import sds011

def run():
    lcd = GpioLcd(rs_pin=Pin(16),
                  enable_pin=Pin(5),
                  d4_pin=Pin(14),
                  d5_pin=Pin(12),
                  d6_pin=Pin(13),
                  d7_pin=Pin(15),
                  num_lines=2, num_columns=16)
    lcd.clear()
    new_term = None
    while True:
        # dupterm allows us to use TX/RX for the sds011 read, then restore TX/RX to the web REPL.
        old_term = uos.dupterm(new_term, 1)

        # Read the two measurements from the SDS011.
        readings = sds011.read(1)
        new_term = uos.dupterm(old_term, 1)

        if readings is not None:
            pm25, pm10 = readings
            lcd.move_to(0, 0)
            message = "PM2.5 %3d ug/m3\nPM10 %4d ug/m3" % (pm25, pm10)
            lcd.putstr(message)
            print(message)

        sleep(1)
