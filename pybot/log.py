import threading
import time
import os

_initialized = False
_log_file_lock = threading.Lock ()

def write ( text ):
    """Append a line to the logfile and add a timestamp.

    This method is thread safe.
    """

    with _log_file_lock:
        # Open file in append mode so no old lines are lost
        with open ( "pybot.log", "a" ) as f:
            timestamp = time.strftime ( "%H:%M:%S", time.localtime () )
            f.write ( "%s: %s\n" % ( timestamp, text ) )


# Initialize log
with open ( os.path.dirname ( __file__ ) + "/../pybot.log", "w" ) as f:
    pass
