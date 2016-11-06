#!/usr/bin/env python
#-*- coding: cp866 -*-

# script to test additional characters. New symbols should be aaded to font.py 
# line 2 is needed to support additional character table. In our case cp866 is required to support Cyrillic. 

import sys
import time

import scrollphat

scrollphat.set_brightness(2)

# we want to test whether all the characters are shown correctly. String is converted from cp866 to Unicode, utf-8 is used for Cyrillic
pr = "Съешь еще этих мягких французских булок, да выпей же чаю.    ".decode('utf-8')
print(pr)

scrollphat.write_string(pr)
while True:
    try:
        scrollphat.scroll()
        time.sleep(0.05)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
