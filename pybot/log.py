import threading
import time
import os

_log_file_lock = threading.Lock ()

def initialize ():
    """Truncate the file by opening it in write mode."""

    # This loads the right file regardless from where the bot was started
    with open ( os.path.dirname ( __file__ ) + "/../pybot.log", "w" ) as f:
        pass

def write ( text ):
    """Append a line to the logfile and add a timestamp.

    This method is thread safe.
    """

    with _log_file_lock:
        # Open file in append mode so no old lines are lost
        with open ( "pybot.log", "a" ) as f:
            timestamp = time.strftime ( "%H:%M:%S", time.localtime () )
            f.write ( "%s: %s\n" % ( timestamp, text ) )

