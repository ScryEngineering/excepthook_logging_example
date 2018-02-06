import sys
import logging
import threading

from threaded_exception import RunsInAThread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Handler for unhandled exceptions that will write to the logs"""
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_unhandled_exception



try:
    raise ValueError("we catch this one")
except ValueError:
    logger.info("Caught the exception")


# Test that the logger get exception raised from thread
foo = RunsInAThread("Runs on thread")
thread = threading.Thread(target=foo.run, args=())
thread.daemon = True
thread.start()
thread.join()
