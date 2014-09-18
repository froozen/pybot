import time

logname = "pybot_log"

def open_log():
    f = open(logname, 'w')
    f.write("Starting at: " + time.strftime("[%H:%M, %d.%m]") +'\n' )
    f.close

def append_to_log(string):
    f = open(logname, 'a')
    f.write(time.strftime("[%H:%M, %d.%m] ") + string + '\n')
    f.close

def init():
    open_log()
