import sys
import logging
import threading

from threaded_exception import RunsInAThread

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

def handle_unhandled_exception(exc_type, exc_value, exc_traceback, thread_identifier=''):
    """Handler for unhandled exceptions that will write to the logs"""
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    if not thread_identifier:
        logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
    else:
        logger.critical("Unhandled exception (on thread %s)", thread_identifier, exc_info=(exc_type, exc_value, exc_traceback))
        

sys.excepthook = handle_unhandled_exception


def patch_threading_excepthook():
    """Installs our exception handler into the threading
    Inspired by https://bugs.python.org/issue1230540
    """
    old_init = threading.Thread.__init__
    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        old_run = self.run
        def run_with_our_excepthook(*args, **kwargs):
            try:
                old_run(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info(), thread_identifier=threading.get_ident())
        self.run = run_with_our_excepthook
    threading.Thread.__init__ = new_init

patch_threading_excepthook()

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
