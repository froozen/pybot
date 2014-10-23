import log
import socket
import configuration
import re

class Irc_server ( object ):
    def __init__ ( self, configuration_handle ):
        """Create an Irc_server from a Configuration_handle.

        Used keys:
            host: address of the server
            port: port of the server ( optional )
        """

        # Used in _read_line
        self._last_lines = []

        if not type ( configuration_handle ) == configuration.Configuration_handle:
            log.write ( "Error in irc: configuration_handle is not a Configuration_handle" )
            raise ValueError ( "Error: configuration_handle is not a Configuration_handle" )

        # Assume this as a default value
        self.port = 6667
        self.host = configuration_handle.get ( "host" )

        # Use port from configuration if it exists
        if configuration_handle.get ( "port" ):
            self.port = configuration_handle.get ( "port" )

        self._socket = socket.socket ()

        try:
            # Connect to server
            self._socket.connect ( ( self.host, self.port ) )

        except socket.error:
            log.write ( "Error in irc: Failed to connect to server: %s:%d" % ( self.host, self.port ) )
            raise

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
