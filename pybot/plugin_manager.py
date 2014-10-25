import threading
import pkgutil
import plugins
import log

command_prefix = ")"
_allow_register = False
_event_handling = {}
_commands = {}

class Command ( object ):
    def __init__ ( self, event ):
        self.event = event

        parts = event.args [ 1 ].split ( " " )
        self.name = parts [ 0 ] [ 1: ]
        self.args = parts [ 1: ]

def load_plugins ():
    global _allow_register
    _allow_register = True

    log.write ( "Loading plugins." )

    for importer, module_name, is_pkg in pkgutil.iter_modules ( plugins.__path__, "%s." % plugins.__name__ ):
        module = __import__ ( module_name, fromlist = "dummy" )
        log.write ( "Imported %s" % module.__name__ )

    _allow_register = False

def register_event_handler ( event, handler ):
    """Register handlier method for an event.

    This will only work while the plugins are being imported.
    """

    if _allow_register:
        # Create list if there is none
        if not event in _event_handling:
            _event_handling [ event ] = []

        _event_handling [ event ].append ( handler )

def register_command ( command, method ):
    """Register method to represent a command.

    This will only work while the plugins are being imported.
    """

    if _allow_register:
        # Command doesn't collide with an already registered one
        if not command in _commands:
            _commands [ command ] = method

        else:
            log.write ( "Error: command \"%s\" is already registered." % command )

def handle_event ( event, server ):
    """Handle a received event.

    This method is thread safe.
    """

    if event.type in _event_handling:
        for handler in _event_handling [ event.type ]:
            _dispatch ( handler, event, server )

    if event.type == "PRIVMSG":
        # Qualifies as command
        if event.args [ 1 ].startswith ( command_prefix ):
            command = Command ( event )
            if command.name in _commands:
                _dispatch ( _commands [ command.name ], command, server )

def _dispatch ( method, *args ):
    """Run method with args in another thread."""

    t = threading.Thread ( target = method, args = args )
    t.daemon = True
    t.start ()
