import log
import socket
import re
from data_container import Data_container

class Irc_server ( object ):
    def __init__ ( self, data_container ):
        """Create an Irc_server from a Data_container.

        Used keys:
            host: address of the server
            port: port of the server ( optional )
            nick: nickname the bot will use
        """

        # Used in _read_line
        self._last_lines = []

        if not type ( data_container ) == Data_container:
            log.write ( "Error in irc: data_container is not a Data_container" )
            raise ValueError ( "Error: data_container is not a Data_container" )

        # Assume this as a default value
        self.port = 6667
        self.host = data_container.get ( "host" )
        self.nick = data_container.get ( "nick" )

        # Use port from configuration if it exists
        if data_container.get ( "port" ):
            self.port = data_container.get ( "port" )

        self._socket = socket.socket ()

        try:
            # Connect to server
            self._socket.connect ( ( self.host, self.port ) )

        except socket.error:
            log.write ( "Error in irc: Failed to connect to server: %s:%d" % ( self.host, self.port ) )
            raise

        self._register ()

    def _register ( self ):
        """Register using NICK and USER, then wait for MODE signal"""

        nick_event = Irc_event ( "NICK", self.nick )
        self.send_event ( nick_event )
        user_event = Irc_event ( "USER", self.nick, "localhost", "localhost", "irc bot" )
        self.send_event ( user_event )

        while True:
            event = self.get_next_event ()

            if event.type == "MODE" and event.args == [ self.nick, "+i" ]:
                break

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

    def get_next_event ( self ):
        """Return the Irc_event corresponding to the next line."""
        line = self._read_line ()
        return Irc_event ( line )

    def send_event ( self, event ):
        if not type ( event ) == Irc_event:
            log.write ( "Error in irc: event is not an Irc_event" )
            raise ValueError ( "Error: event is not an Irc_event" )

        self._socket.send ( "%s\r\n" % event.signal )

class Irc_event ( object ):
    def __init__ ( self, line_o_type = None, *args ):
        """Create an Irc_event

        Possible calls:
            line:                     parses a line from the irc-protocoll
            type, arg1, arg2, arg...: Create your own event
        """

        # Set default values
        self.name = None
        self.host = None
        self.type = None
        self.args = []

        if len ( args ) == 0:
            parts = line_o_type.split ( " " )

            # Starts with origin
            if parts [ 0 ].startswith ( ":" ):
                # Try to extract the names via regex
                match = re.match ( ":(.*?)!(.*)", parts [ 0 ] )
                if match:
                    self.name = match.group ( 1 )
                    self.host = match.group ( 2 )

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
