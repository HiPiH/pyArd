#!/usr/bin/python3
import serial
import time
import logging


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')



class BaseClass:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def INFO(self, str):
        self.log.info(str)

    def DEBUG(self, str):
        self.log.debug(str)




class MySerial(BaseClass):
    __retry_count__  = 10
    def __init__(self, port='/dev/ttyUSB0', speed=115200):

        super().__init__()

        self.ser = ser = serial.Serial(port, speed, 8, 'N', 1, timeout=1)

        for x in range(0,self.__retry_count__):
            self.INFO(f"Try open port {port}.")
            if not ser.isOpen():
                if x == self.__retry_count__-1:
                    raise Exception(f"Failed open port {port}.")
                time.sleep(0.5)
            else:
                break
        self.INFO(f"Port opened {port}.")
                 
        #reset
        ser.setDTR(False)
        time.sleep(1)
        ser.flushInput()
        ser.setDTR(True)

        #wait ok
        for x in range(0,self.__retry_count__):
            self.INFO(f"Try connect to {port}.")
            ok = self.read()
            if ok != "#ok":
                if x == self.__retry_count__-1:
                    raise Exception(f"Failed connect to {port}.")
                time.sleep(0.5)
            else:
                break
        self.INFO(f"Connected {port}.")


    def read(self):
        ret = self.ser.readline()
        if ret:
            str =  ret.decode('utf-8')[:-1]
            self.DEBUG(f"Read: {ret}")
            return str
        return ""

    def send(self, str):
        self.DEBUG(f"Send: {str}")
        self.ser.write(f"{str}\n".encode())
        return self

        


serial = MySerial()

 
logging.info(serial.send("1111").read())