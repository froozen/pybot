import threading
import log
import json

_config_handle = None
_config_lock = threading.Lock ()

class Configuration_handle ( object ):
    def __init__ ( self, data ):
        """Create a Configuration_handle from a dict."""

        # Configuration_handle will only represent dicts
        if not type ( data ) == dict:
            log.write ( "Error in configuration: data is not a dict" )
            raise ValueError ( "Error: data is not a dict" )

        self._data = data

    def get ( self, key ):
        """Return a configuration value or None if not set

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # Lock to make it thread safe
        _config_lock.acquire ()

        key_levels = key.split ( "." )
        position = self._data

        for key_level in key_levels:
            # Check the current type, so the type of the last iteration's position isn't
            # checked. This will allow getting non-dict values.
            if type ( position ) == dict:
                if key_level in position:
                    # Set position to next dict in "tree"
                    position = position [ key_level ]
                    continue

            # Return None if either one doesn't apply
            return None

        _config_lock.release ()

        return position

    def set ( self, key, value ):
        """Set a configuration value.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        _config_lock.acquire ()

        key_levels = key.split ( "." )
        position = self._data

        # Ommit the last key_level from the iteration so position is the dict we want
        # to save the value in.
        for key_level in key_levels [ : -1 ]:
            if type ( position ) == dict:
                if key_level in position:
                    # Set position to the nex position
                    position = position [ key_level ]

                # Create silently dict if it doesn't exist
                else:
                    position [ key_level ] = {}
                    position = position [ key_level ]

            else:
                log.write ( "Error in configuration: Key_level \"%s\" in path is not a dict" % key_level )
                raise ValueError ( "Error: Key_level \"%s\" in path is not a dict" % key_level )

        # Actually set the value
        position [ key_levels [ -1 ] ] = value

        _config_lock.release ()

    # This is needed for saving the configuration into the config file
    @property
    def _data_string ( self ):
        return json.dumps ( self._data, indent = 4, separators = [ ",", ": " ] )

def initialize ():
    """Load configuration from \"config.json\"."""

    global _config_handle

    try:
        with open ( "config.json" ) as f:
            data = json.loads ( f.read () )
            _config_handle = Configuration_handle ( data )

    except IOError:
        log.write ( "Error in configuration: Failed to load \"config.json\"" )
        raise IOError ( "Error: Failed to load \"config.json\"" )

    except ValueError:
        log.write ( "Error in configuration: Invalid configuration" )
        raise ValueError ( "Error: Invalid configuration" )

def get ( key ):
    """Return a configuration value or None if not set

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _config_handle
    return _config_handle.get ( key )

def set ( key, value ):
    """Set a configuration value.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _config_handle
    _config_handle.set ( key, value )

    # Save changes into file
    with open ( "config.json", "w" ) as f:
        f.write ( _config_handle._data_string )

def get_handle ( key ):
    """Return a Configuration_handle object representing a dict identified by a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    return Configuration_handle ( _config_handle.get ( key ) )
