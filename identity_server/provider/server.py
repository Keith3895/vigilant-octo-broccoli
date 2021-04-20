import logging
from logging.handlers import RotatingFileHandler
import os


path = os.path.join(os.getcwd(),'logs')
try: 
    os.mkdir(path) 
except OSError as error: 
    print(error)   
LOGGER = logging.getLogger("")
LOGFILE_NAME = 'logs/app.log'
hdlr = RotatingFileHandler(LOGFILE_NAME, maxBytes=2000, backupCount=10)
base_formatter = logging.Formatter(
    "%(asctime)s %(name)s:%(levelname)s %(message)s")
hdlr.setFormatter(base_formatter)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.DEBUG)



def main():
    logging.info("in server main")
    print("in main")
    # for _ in range(10000):
    #     logging.warning('Hello, world!')

