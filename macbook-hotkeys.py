#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from evdev import InputDevice, KeyEvent, ecodes
from os import system

dev = InputDevice('/dev/input/event0')

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value in [KeyEvent.key_up, KeyEvent.key_hold]:
            if event.code == ecodes.KEY_BRIGHTNESSDOWN:
                system('expr `cat /sys/class/backlight/intel_backlight/brightness` - 10 > /sys/class/backlight/intel_backlight/brightness')
            if event.code == ecodes.KEY_BRIGHTNESSUP:
                system('expr `cat /sys/class/backlight/intel_backlight/brightness` + 10 > /sys/class/backlight/intel_backlight/brightness')
            if event.code == ecodes.KEY_KBDILLUMDOWN:
                system('expr `cat /sys/class/leds/smc::kbd_backlight/brightness` - 10 > /sys/class/leds/smc::kbd_backlight/brightness')
            if event.code == ecodes.KEY_KBDILLUMUP:
                system('expr `cat /sys/class/leds/smc::kbd_backlight/brightness` + 10 > /sys/class/leds/smc::kbd_backlight/brightness')
