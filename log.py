import threading
import time

_log_file_lock = threading.Lock ()

def initialize ():
    """Truncate the file by opening it in write mode."""

    with open ( "pybot.log", "w" ) as f:
        pass

def write ( text ):
    """Append a line to the logfile and add a timestamp.

    This method is thread safe.
    """

    _log_file_lock.acquire ()

    # Open file in append mode so no old lines are lost
    with open ( "pybot.log", "a" ) as f:
        timestamp = time.strftime ( "%H:%M:%S", time.localtime () )
        f.write ( "%s: %s\n" % ( timestamp, text ) )

    _log_file_lock.release ()

