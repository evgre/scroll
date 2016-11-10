#!/usr/bin/env python
#-*- coding: cp866 -*-

import sys
import time

import scrollphat

# as this starts at boot, we want to give some time for cool animation that plays for 5 seconds from another file
time.sleep(6)
scrollphat.set_brightness(5)

# define the database to read the news from
db = '/home/pi/Pimoroni/scrollphat/feeden.db'
f = open(db)
print iter(f)
while True:
    try:
        for msg in iter(f):
#               this is to ensure no non-ASCII stuff goes through, otherwise program shuts down
                msg = msg.decode('utf-8', errors='ignore').encode('utf-8')
#               check if any text exists on this line exists, otherwise move to next line
                if '|' in msg:
#                       clear buffer of previous message
                        msg = msg.decode('utf-8')
                        scrollphat.clear()
#                       split message in 2 pieces to get rid of timestamp
                        first_p,second_p=msg.split("|")
#                       print only first part before delimeter
                        scrollphat.write_string('       '+ first_p)
                        for i in range(0, scrollphat.buffer_len()):
                                scrollphat.scroll()
                                time.sleep(0.035)
                else: print('no data to show, jumping to next line')
        else:
                f.close()
                f = open(db)
    except KeyboardInterrupt:
        scrollphat.clear()
        f.close()
        sys.exit(-1)
