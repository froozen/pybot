import threading
import time

_log_file_lock = threading.Lock ()

def initialize ():
    with open ( "pybot.log", "w" ) as f:
        pass

def write ( text ):
    _log_file_lock.acquire ()

    with open ( "pybot.log", "a" ) as f:
        timestamp = time.strftime ( "%H:%M:%S", time.localtime () )
        f.write ( "%s: %s\n" % ( timestamp, text ) )

    _log_file_lock.release ()

