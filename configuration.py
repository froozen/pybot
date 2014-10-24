import log
import json
from data_container import Data_container

_config_container = None

def initialize ():
    """Load configuration from \"config.json\"."""

    global _config_container

    try:
        with open ( "config.json" ) as f:
            data = json.loads ( f.read () )
            _config_container = Data_container ( data )

    except IOError:
        log.write ( "Error in configuration: Failed to load \"config.json\"" )
        raise

    except ValueError:
        log.write ( "Error in configuration: Invalid configuration" )
        raise

def get ( key ):
    """Return a configuration value or None if not set

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _config_container
    return _config_container.get ( key )

def set ( key, value ):
    """Set a configuration value.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _config_container
    _config_container.set ( key, value )
    save ()

def get_data_container ( key ):
    """Return a Data_container object representing a dict identified by a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    return _config_container.get_data_container ( key )

def save ():
    """Save the configuration data back into \"config.json\"

    This method is thread safe
    """

    # Save changes into file
    with open ( "config.json", "w" ) as f:
        f.write ( json.dumps ( _config_container.get_data (), indent = 4, separators = [ ",", ": " ] ) )
