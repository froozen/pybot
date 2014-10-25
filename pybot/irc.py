import os
import re
import log
import time
import users
import socket
import threading
import plugin_manager
from configuration import Configuration_data_container
from data_container import Data_container, Persistent_data_container

class Irc_server ( threading.Thread ):
    def __init__ ( self, data_container ):
        """Create an Irc_server from a Data_container.

        Used keys:
            host: address of the server
            port: port of the server ( optional )
            nick: nickname the bot will use
            channels: channels to join upon connect ( optional )
        """


        # Do all the Thread related things
        threading.Thread.__init__ ( self )
        self.daemon = True

        # Used in _read_line
        self._last_lines = []

        self.user_data = users.User_data ( self )
        self.shared_data = Data_container ( {} )

        if not type ( data_container ) == Data_container:
            log.write ( "Error in irc: data_container is not a Data_container" )
            raise ValueError ( "Error: data_container is not a Data_container" )

        # Assume this as a default value
        self.port = 6667
        self.host = data_container.get ( "host" )
        self.prefered_nick = data_container.get ( "nick" )
        self._channels = []
        self.nick = None

        # Make sure server_data exists
        if not os.path.isdir ( os.path.dirname ( __file__ ) + "/../server_data" ):
            os.makedirs ( os.path.dirname ( __file__ ) + "/../server_data" )

        # Load server config
        self.cofiguration = Configuration_data_container ( os.path.dirname ( __file__ ) + "/../server_data/%s.config.json" % self.host )
        self.persistent_data = Persistent_data_container ( os.path.dirname ( __file__ ) + "/../server_data/%s.data.json" % self.host )

        # Use port from configuration if it exists
        if data_container.get ( "port" ):
            self.port = data_container.get ( "port" )

        if data_container.get ( "channels" ):
            self._channels = data_container.get ( "channels" )

    def run ( self ):
        while True:
            self._connect ()
            while True:
                event = self._next_event ()
                plugin_manager.handle_event ( event, self )

    def _connect ( self ):
        """Connect to server via socket."""

        sleep_time = 15

        while True:
            self._socket = socket.socket ()
            # Set timeout for disconnecte detection
            self._socket.settimeout ( 250 )

            try:
                # Connect to server
                self._socket.connect ( ( self.host, self.port ) )
                log.write ( "%s: Connection established" % self.host )
                break

            except socket.error:
                log.write ( "%s: Error in irc: Connecting failed." % self.host )

            log.write ( "%s: Retrying in %ds." % ( self.host, sleep_time ) )
            time.sleep ( sleep_time )
            sleep_time = sleep_time * 2 if sleep_time * 2 < 300 else 300

        self._register ()

    def _register ( self ):
        """Register using NICK and USER, then wait for MODE signal and JOIN the channels"""

        self.nick = self.prefered_nick

        nick_event = Irc_event ( "NICK", self.nick )
        self.send_event ( nick_event )
        user_event = Irc_event ( "USER", self.nick, "localhost", "localhost", "irc bot" )
        self.send_event ( user_event )

        while True:
            event = self._next_event ()

            if event.type == "MODE" and event.args [ 0 ] == self.nick:
                log.write ( "%s: Connected as %s" % ( self.host, self.nick ) )
                # Automaticly join channels
                if len ( self._channels ) > 0:
                    join_event = Irc_event ( "JOIN", ",".join ( self._channels ) )
                    self.send_event ( join_event )
                break

            # Nick already in use
            elif event.type == "433":
                log.write ( "%s: %s already taken, switching to %s_." % ( self.host, self.nick, self.nick ) )
                self.nick = "%s_" % self.nick
                nick_event = Irc_event ( "NICK", self.nick )
                self.send_event ( nick_event )

    def _read_line ( self ):
        """Read one irc-line from self._socket"""

        # The loop will be ended by the return statement
        while True:
            if len ( self._last_lines ) > 0:
                # A line ending in a linebreak means that it's a full line
                if self._last_lines [ 0 ].endswith ( "\r" ):
                    # Return the next line and remove the linebreak
                    return self._last_lines.pop ( 0 ) [ : -1 ]

            buffer = self._socket.recv ( 1024 )
            lines = buffer.split ( "\n" )

            # If there is an incomplete line left
            if len ( self._last_lines ) > 0:
                # Add the first complete line to the incomplete one
                self._last_lines [ 0 ] += lines.pop ( 0 )

            # Add the rest of the lines
            if len ( lines ) > 0:
                self._last_lines.extend ( lines )

    def _next_event ( self ):
        """Return the Irc_event corresponding to the next line."""

        try:
            line = self._read_line ()
        except socket.timeout:
            line = "DISCONNECT %s" % time.ctime ()

        event = Irc_event ( line )

        # Try to call event handling function
        for target in [ "self", "self.user_data" ]:
            try:
                exec "%s._on_%s ( event )" % ( target, event.type.lower () )

            except AttributeError:
                pass

        return event

    def _on_disconnect ( self, event ):
        """Automaticly reconnect upon disconnect."""

        log.write ( "%s: Connection lost." % self.host )
        self._connect ()

    def send_event ( self, event ):
        """Send event over socket."""

        if not type ( event ) == Irc_event:
            log.write ( "Error in irc: event is not an Irc_event" )
            raise ValueError ( "Error: event is not an Irc_event" )

        self._socket.send ( "%s\r\n" % event.signal )

    def _on_ping ( self, event ):
        """Automaticly handle pings."""

        pong_event = Irc_event ( "PONG", event.args [ 0 ] )
        self.send_event ( pong_event )

    def _on_join ( self, event ):
        """Keep track of joined channels to join upon reconnect."""

        if event.name == self.nick:
            if event.args [ 0 ] in self._channels:
                self._channels.append ( event.args [ 0 ] )

    def _on_part ( self, event ):
        """Keep track of joined channels to join upon reconnect."""

        if event.name == self.nick:
            self._channels.remove ( event.args [ 0 ] )

    def _on_nick ( self, event ):
        """Keep track of own nick."""

        if event.name == self.nick:
            self.nick = event.args [ 0 ]

class Irc_event ( object ):
    def __init__ ( self, line_o_type = None, *args ):
        """Create an Irc_event

        Possible calls:
            line:                     parses a line from the irc-protocoll
            type, arg1, arg2, arg...: Create your own event
        """

        # Set default values
        self.name = None
        self.user = None
        self.host = None
        self.type = None
        self.args = []

        if len ( args ) == 0:
            parts = line_o_type.split ( " " )

            # Starts with origin
            if parts [ 0 ].startswith ( ":" ):
                # Try to extract the names via regex
                match = re.match ( ":(.*?)!(?:(.*?)@(.*))", parts [ 0 ] )
                if match:
                    self.name = match.group ( 1 )
                    self.user = match.group ( 2 )
                    self.host = match.group ( 3 )

                # Save the whole as name
                else:
                    self.name = parts [ 0 ] [ 1: ]

                # Remove this part
                parts.pop ( 0 )

            self.type = parts.pop ( 0 )

            # Iterate over arguments
            for i in range ( len ( parts ) ):
                # Last argument
                if parts [ i ].startswith ( ":" ):
                    # Remove the ":"
                    parts [ i ] = parts [ i ] [ 1: ]
                    self.args.append ( " ".join ( parts [ i: ] ) )
                    break
                else:
                    self.args.append ( parts [ i ] )

        else:
            self.type = line_o_type
            self.args = args

    @property
    def signal ( self ):
        signal = self.type

        for arg in self.args:
            # Last argument
            if " " in arg:
                signal += " :%s" % arg
                break

            else:
                signal += " " + arg
        return signal
