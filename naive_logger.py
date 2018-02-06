import sys
import logging
import threading

from threaded_exception import RunsInAThread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='naive.log', filemode='w', level=logging.DEBUG)



try:
    foo = RunsInAThread("Runs on thread")
    thread = threading.Thread(target=foo.run, args=())
    thread.daemon = True
    thread.start()
    thread.join()
except:
    logger.critical("Unhandled exception:", exc_info=sys.exc_info())
    raise
