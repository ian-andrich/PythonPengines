import logging
import sys

class TestingStreamHandler(logging.StreamHandler):

    @property
    def stream(self):
        return sys.stdout

    @stream.setter
    def stream(self, value): pass

def log_tests(level):
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = TestingStreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(ch)

