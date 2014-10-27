#!/usr/bin/env python2

from pybot import configuration, irc, log, plugin_manager
from pybot.data_container import Data_container
import time

plugin_manager.load_plugins ()

servers = configuration.get ( "servers" )
for server_config in servers:
    handle = Data_container ( server_config )
    server = irc.Irc_server ( handle )
    server.start ()

while True:
    # Keep thread alive
    time.sleep ( 1 )
