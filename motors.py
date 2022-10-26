from myserial import MySerial
from baseclass import BaseClass

class Motors(BaseClass):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial
    

