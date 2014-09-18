#!/usr/bin/python2

import connection
import plugin_handler
import logging

logging.init()
connection.init()
plugin_handler.init()

while True:
    readlines = connection.read_lines()
    
    for readline in readlines:
        plugin_handler.handle_input(readline)

connection.disconnect()
