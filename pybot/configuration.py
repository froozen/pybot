import log
import json
import os
from persistent_data import Persistent_data_container

_config_container = None


class Configuration_data_container (object):

    def __init__(self, filename):
        """Create a Configuration_data_container from a filename."""

        self._container = Persistent_data_container(filename)

    def get(self, key):
        """Return a value or None if not set

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get(key)

    def get_data(self):
        """Return a deepcopy of the wrapped data.

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get_data()

    def get_data_container(self, key):
        """Return a Data_container object representing a dict identified by a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # Simply return value from self._container
        return self._container.get_data_container(key)


def get(key):
    """Return a configuration value or None if not set

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _config_container
    return _config_container.get(key)


def get_data_container(key):
    """Return a Data_container object representing a dict identified by a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    return _config_container.get_data_container(key)

# Initialize configuration
if _config_container == None:
    _config_container = Configuration_data_container(
        os.path.dirname(__file__) + "/../config.json")
