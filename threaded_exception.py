class ExceptionFromThread(Exception):
    """An exception type we raise from within a thread"""

class RunsInAThread:
    def __init__(self, error_message):
        self.error_message = error_message

    def run(self):
        raise ExceptionFromThread(self.error_message)
