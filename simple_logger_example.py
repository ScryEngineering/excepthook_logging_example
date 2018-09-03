import sys
import logging
import threading

from threaded_exception import RunsInAThread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='simple.log', filemode='w', level=logging.DEBUG)

logger.debug("This is an debug message")
logger.info("This is an info message")
logger.warning("This is an warning message")
logger.critical("This is an critical message")

