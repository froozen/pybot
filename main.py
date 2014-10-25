#!/usr/bin/python2

from pybot import configuration, irc, log, plugin_manager
import time

plugin_manager.load_plugins ()

servers = configuration.get ( "servers" )
for server_name in servers:
    handle = configuration.get_data_container ( "servers.%s" % server_name )
    server = irc.Irc_server ( handle )
    server.start ()

while True:
    # Keep thread alive
    time.sleep ( 1 )
