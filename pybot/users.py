import threading
import log
import irc

class User ( object ):
    def __init__ ( self, nick ):
        """Create User from a nickname.

        The leading \"@\" for ops is removed.
        """

        self.nick = nick
        self.channels = []
        self.host = None

        # Remove op symbol
        if self.nick.startswith ( "@" ):
            self.nick = self.nick [ 1: ]

class Channel ( object ):
    def __init__ ( self, name ):
        """Create Channel."""

        self.name = name
        self.users = []
        self.ops = []

class User_data ( object ):
    # Outline:
    # users: map of users by name
    # channels: map of channels by name

    def __init__ ( self, server ):
        """Create User_data for a server."""

        if not type ( server ) == irc.Irc_server:
            log.write ( "Error in rebuild: server is not a Irc_server" )
            raise ValueError ( "Error: server is not a Irc_server" )

        self._server = server
        self._lock = threading.Lock ()
        self._users = {}
        self._channels = {}

    def _on_join ( self, event ):
        """Handle JOIN events."""

        with self._lock:
            # Bot joined a channel
            if event.name == self._server.nick:
                log.write ( "%s: Joined %s" % ( self._server.host, event.args [ 0 ] ) )
                # Add new channel
                self._channels [ event.args [ 0 ] ] = Channel ( event.args [ 0 ] )

            else:
                user = None

                # Create user if it doesn't exist
                if not event.name in self._users:
                    user = User ( event.name )
                    self._users [ event.name ] = user

                else:
                    user = self._users [ event.name ]

                user.channels.append ( event.args [ 0 ] )

                # Add user to channel
                self._channels [ event.args [ 0 ] ].users.append ( user )

    def _on_part ( self, event ):
        """Handle PART events."""

        with self._lock:
            user = self._users [ event.name ]
            channel = self._channels [ event.args [ 0 ] ]

            # User left his only known channel
            if len ( user.channels ) == 1:
                # Remove user
                del self._users [ event.name ]

            else:
                # Remove channel from users channels
                user.channels.remove ( event.args [ 0 ] )

            # Remove user from channel
            channel.users.remove ( user )

            # Remove user from ops
            if user in channel.ops:
                channel.ops.remove ( user )

    def _on_quit ( self, event ):
        """Handle QUIT events."""

        # Those two methods do exactly the same thing
        self._on_part ( event )

    def _on_nick ( self, event ):
        """Handle NICK events."""

        with self._lock:
            # The channel doesn't need to be modified, because
            # only has a reference to the user object instead
            # of strings

            user = self._users [ event.name ]

            # Change the users nick
            user.nick = event.args [ 0 ]

            # Move user over
            del self._users [ event.name ]
            self._users [ event.args [ 0 ] ] = user

    # NAMES signal, send when joining a new channel
    def _on_353 ( self, event ):
        """Handle 353 events. ( NAMES response )"""

        with self._lock:
            channel = self._channels [ event.args [ 2 ] ]
            nicks = event.args [ 3 ].split ( " " )

            for nick in nicks:
                # Take advantage of User removing the "@" at the begining
                user = User ( nick )

                # User is not known yet
                if not user.nick in self._users:
                    self._users [ user.nick ] = user
                else:
                    user = self._users [ user.nick ]

                user.channels.append ( channel.name )
                channel.users.append ( user )

                # User is op
                if nick.startswith ( "@" ):
                    channel.ops.append ( user )

    # WHOIS host response
    def _on_311 ( self, event ):
        """Handle 311 events. ( WHOIS host response )"""

        with self._lock:
            # Some plugin might use the WHOIS command on unknown users
            if event.args [ 1 ] in self._users:
                self._users [ event.args [ 1 ] ].host = "%s@%s" % ( event.args [ 2 ], event.args [ 3 ] )

    def _on_mode ( self, event ):
        """Handle MODE events."""

        with self._lock:
            # Only handle modes on channels
            if event.args [ 0 ] in self._channels:
                channel = self._channels [ event.args [ 0 ] ]
                user = self._users [ event.name ]

                # User receives op
                if event.args [ 1 ].startswith ( "+" ) and "o" in event.args [ 1 ]:
                    channel.ops.append ( user )

                # User loses op
                elif event.args [ 1 ].startswith ( "-" ) and "o" in event.args [ 1 ]:
                    channel.ops.remove ( user )
