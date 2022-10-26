#!/usr/bin/python3
from myserial import MySerial
from motors import Motors
import logging
import time
#python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000


serial = MySerial('/dev/ttyUSB0')
# logging.info(serial.sendFB([0,0,0,0,0]).read())
# motors = Motors(serial)
serial.loop.start()
serial.sendFB([0,0,0,0,0.5])
time.sleep(2)
serial.sendFB([0,0,0,0,0])

# serial.sendFB([1,0,0,0,0])

# serial.sendFB([0,0,0,0,0])

serial.loop.join()
serial.__enable__ = False

