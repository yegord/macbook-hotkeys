#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import evdev
import glob
import os
import select

class Backlight(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.brightness_filename = os.path.join(self.dirname, 'brightness')
        self.max_brightness_filename = os.path.join(self.dirname, 'max_brightness')

    def get_min_brightness(self):
        return 0

    def get_max_brightness(self):
        with open(self.max_brightness_filename, 'r') as f:
            return int(f.read())

    def get_brightness(self):
        with open(self.brightness_filename, 'r') as f:
            return int(f.read())

    def set_brightness(self, value):
        value = max(value, self.get_min_brightness())
        value = min(value, self.get_max_brightness())
        with open(self.brightness_filename, 'w') as f:
            f.write(str(value))

    def increase_brightness(self, delta):
        self.set_brightness(self.get_brightness() + delta)

    def decrease_brightness(self, delta):
        self.increase_brightness(-delta)

if __name__ == '__main__':
    screen = Backlight('/sys/class/backlight/intel_backlight')
    keyboard = Backlight('/sys/class/leds/smc::kbd_backlight')

    screen_delta = 20
    keyboard_delta = 10

    devs = [
        evdev.InputDevice(filename)
        for filename in glob.glob('/dev/input/event*')
    ]

    poller = select.poll()
    for dev in devs:
        poller.register(dev, select.POLLIN)

    fileno_to_dev = {dev.fileno(): dev for dev in devs}

    while True:
        for fileno, status in poller.poll():
            dev = fileno_to_dev[fileno]
            event = dev.read_one()
            if event.type == evdev.ecodes.EV_KEY:
                if event.value in [evdev.KeyEvent.key_up, evdev.KeyEvent.key_hold]:
                    if event.code == evdev.ecodes.KEY_BRIGHTNESSDOWN:
                        screen.decrease_brightness(screen_delta)
                    if event.code == evdev.ecodes.KEY_BRIGHTNESSUP:
                        screen.increase_brightness(screen_delta)
                    if event.code == evdev.ecodes.KEY_KBDILLUMDOWN:
                        keyboard.decrease_brightness(keyboard_delta)
                    if event.code == evdev.ecodes.KEY_KBDILLUMUP:
                        keyboard.increase_brightness(keyboard_delta)
