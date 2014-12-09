import threading
import copy
import log
import irc

class User ( object ):
    def __init__ ( self, nick ):
        """Create User from a nickname."""

        self.nick = nick
        self.channels = []
        self.host = None

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

    def get_user ( self, nick ):
        """Return User object corresponding to nick or None.

        This method is thread safe.
        """

        with self._lock:
            if nick in self._users:
                # Return a deepycopy to be thread safe
                return copy.deepcopy ( self._users [ nick ] )
            else:
                return None

    def get_channel ( self, channel ):
        """Return Channel object corresponding to name on None.

        This method is thread safe.
        """

        with self._lock:
            if channel in self._channels:
                # Return a deepycopy to be thread safe
                return copy.deepcopy ( self._channels [ channel ] )
            else:
                return None

    def _on_join ( self, event ):
        """Handle JOIN events."""

        with self._lock:
            channel_name = event.args [ 0 ]

            # Bot joined a channel
            if event.name == self._server.nick:
                log.write ( "%s: Joined %s" % ( self._server.host, channel_name ) )

            else:
                self._add_user_to_channel ( event.name, channel_name )

    def _on_part ( self, event ):
        """Handle PART events."""

        with self._lock:
            self._remove_user_from_channel ( event.name, event.args [ 0 ] )

    def _on_quit ( self, event ):
        """Handle QUIT events."""

        with self._lock:
            user =  self._users [ event.name ]

            # Removing the user from every channel they are on will delete them
            for channel_name in user.channels:
                self._remove_user_from_channel ( event.name, channel_name )

    def _on_nick ( self, event ):
        """Handle NICK events."""

        with self._lock:
            # The channel doesn't need to be modified, because
            # only has a reference to the user object instead
            # of strings

            user = self._users [ event.name ]
            new_nick = event.args [ 0 ]

            # Change the users nick
            user.nick = new_nick

            # Move user over
            del self._users [ event.name ]
            self._users [ new_nick ] = user

    # NAMES signal, send when joining a new channel
    def _on_353 ( self, event ):
        """Handle 353 events. ( NAMES response )"""

        with self._lock:
            channel_name = event.args [ 2 ]
            nicks = event.args [ 3 ].split ( " " )

            for nick in nicks:
                # Add every nick to the channel
                self._add_user_to_channel ( nick, channel_name )

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
                if event.name in self._users:
                    channel = self._channels [ event.args [ 0 ] ]
                    user = self._users [ event.name ]

                    # User receives op
                    if event.args [ 1 ].startswith ( "+" ) and "o" in event.args [ 1 ]:
                        channel.ops.append ( user )

                    # User loses op
                    elif event.args [ 1 ].startswith ( "-" ) and "o" in event.args [ 1 ]:
                        channel.ops.remove ( user )

    def _on_dicsconnect ( self, event ):
        """Handle disconnect by wiping out everything."""

        with self._lock:
            # Reset all known data
            self._channels = {}
            self._users = {}

    def _add_user_to_channel ( self, nick, channel_name ):
        """Add a user to a channel.

        Create everything that doesn't exist yet.
        """

        # Check for op and fix nick, if neccessary
        is_op = False
        if nick.startswith ( "@" ):
            is_op = True
            nick = nick [ 1: ]

        # Add channel if it doesn't exist
        if not channel_name in self._channels:
            self._add_channel ( channel_name )

        # Add user if they don't exist
        if not nick in self._users:
            self._add_user ( nick )

        # Add channel to user
        user = self._users [ nick ]
        user.channels.append ( channel_name )

        # Add user to channel
        channel = self._channels [ channel_name ]
        channel.users.append ( user )

        # Add them to ops as well if they are one
        if is_op:
            channel.ops.append ( user )

    def _add_channel ( self, channel_name ):
        """Add a new channel."""

        # Create the new channel
        self._channels [ channel_name ] = Channel ( channel_name )

    def _add_user ( self, nick ):
        """Add a new user."""

        # Create the new user
        self._users [ nick ] = User ( nick )

        # Send WHOIS event to get their host
        whois_event = irc.Irc_event ( "WHOIS", nick )
        self._server.send_event ( whois_event )

    def _remove_user_from_channel ( self, nick, channel_name ):
        """Remove user from a channel.

        Delete anything that isn't needed anymore.
        """

        user = self._users [ nick ]
        channel = self._channels [ channel_name ]

        # Remove references to each other
        channel.users.remove ( user )
        user.channels.remove ( channel_name )

        # Remove user from ops, if they are op
        if user in channel.ops:
            channel.ops.remove ( user )

        # User is "unknown"
        if len ( user.channels ) == 0:
            del self._users [ nick ]
