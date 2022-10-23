import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')


class BaseClass:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def INFO(self, str):
        self.log.info(str)

    def DEBUG(self, str):
        self.log.debug(str)