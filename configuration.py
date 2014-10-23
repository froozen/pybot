import threading
import log
import json

_config_handle = None
_config_lock = threading.Lock ()

class Configuration_handle ( object ):
    def __init__ ( self, data ):
        if not type ( data ) == dict:
            log.write ( "Error in configuration: data is not a dict" )
            raise ValueError ( "Error: data is not a dict" )

        self._data = data

    def get ( self, key ):
        _config_lock.acquire ()

        key_levels = key.split ( "." )
        position = self._data

        for key_level in key_levels:
            if type ( position ) == dict:
                if key_level in position:
                    position = position [ key_level ]
                    continue

            return None

        _config_lock.release ()

        return position

    def set ( self, key, value ):
        _config_lock.acquire ()

        key_levels = key.split ( "." )
        position = self._data

        for key_level in key_levels [ : -1 ]:
            if type ( position ) == dict:
                if key_level in position:
                    position = position [ key_level ]
                    continue

                else:
                    position [ key_level ] = {}
                    position = position [ key_level ]

            else:
                log.write ( "Error in configuration: Key_level \"%s\" in path is not a dict" % key_level )
                raise ValueError ( "Error: Key_level \"%s\" in path is not a dict" % key_level )

        position [ key_levels [ -1 ] ] = value

        _config_lock.release ()

    @property
    def _data_string ( self ):
        return json.dumps ( self._data, indent = 4, separators = [ ",", ": " ] )

def initialize ():
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
    return _config_handle.get ( key )

def set ( key, value ):
    _config_handle.set ( key, value )

    with open ( "config.json", "w" ) as f:
        f.write ( _config_handle._data_string )

def get_handle ( key ):
    return Configuration_handle ( _config_handle.get ( key ) )
