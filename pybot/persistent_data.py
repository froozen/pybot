from data_container import Data_container
import threading
import json
import os

class Persistent_data_container ( object ):
    def __init__ ( self, filename ):
        """Create a Persistent_data from a filename"""

        self.filename = filename
        self._lock = threading.Lock ()

        data = {}
        # Check wether file exists
        if os.path.isfile ( filename ):
            # Load data from file
            try:
                with open ( filename ) as f:
                    data = json.loads ( f.read () )

            except IOError:
                log.write ( "Error in data_container: Failed to load \"%s\"" % filename )
                raise

            except ValueError:
                log.write ( "Error in data_container: Invalid JSON in \"%s\"" % filename )
                raise

        self._container = Data_container ( data )

    def set ( self, key, value ):
        """Set a value.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        self._container.set ( key, value )
        self._save ()

    def append ( self, key, value ):
        """Append a value to a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        self._container.append ( key, value )
        self._save ()

    def pop ( self, key, index ):
        """Pop the value at an index off a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        self._container.pop ( key, index )
        self._save ()

    def remove ( self, key, value ):
        """Remove a value from a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        self._container.remove ( key, value )
        self._save ()

    def _save ( self ):
        """Save the data to the container."""

        with self._lock:
            try:
                # Write data into file
                with open ( self.filename, "w" ) as f:
                    f.write ( json.dumps ( self._container.get_data (), indent = 4, separators = [ ",", ": " ] ) )

            except IOError:
                log.write ( "Error in data_container: Failed to open \"%s\"" % filename )
                raise

    def get ( self, key ):
        """Return a value or None if not set

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get ( key )

    def get_data ( self ):
        """Return a deepcopy of the wrapped data.

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get_data ()

    def get_data_container ( self, key ):
        """Return a Data_container object representing a dict identified by a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get_data_container ( key )

def get ( key ):
    """Return a value or None if not set

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    return _container.get ( key )

def set ( key, value ):
    """Set a value.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.set ( key, value )

def get_data_container ( key ):
    """Return a Data_container object representing a dict identified by a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    return _container.get_data_container ( key )

def append ( self, key, value ):
    """Append a value to a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.append ( key, value )

def pop ( self, key, index ):
    """Pop the value at an index off a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.pop ( key, index )

def remove ( self, key, value ):
    """Remove a value from a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.remove ( key, value )

_container = Persistent_data_container ( os.path.dirname ( __file__ ) + "/../.persistent_data.json" )
