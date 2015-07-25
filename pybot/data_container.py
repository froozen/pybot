import os
import copy
import threading
import log
import json


class Data_container (object):

    def __init__(self, data):
        """Create a Data_container from a dict."""

        # Data_container will only represent dicts
        if not type(data) == dict:
            log.write("Error in data_container: data is not a dict")
            raise ValueError("Error: data is not a dict")

        # Always use deepcopy to make it thread safe
        self._data = copy.deepcopy(data)
        self._lock = threading.Lock()

    def get(self, key):
        """Return a value or None if not set

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        with self._lock:
            key_levels = key.split(".")
            position = self._data

            for key_level in key_levels:
                # Check the current type, so the type of the last iteration's position isn't
                # checked. This will allow getting non-dict values.
                if type(position) == dict:
                    if key_level in position:
                        # Set position to next dict in "tree"
                        position = position[key_level]
                        continue

                # Return None if either one doesn't apply
                return None

            # Always use deepcopy to make it thread safe
            return copy.deepcopy(position)

    def append(self, key, value):
        """Append a value to a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        with self._lock:
            key_levels = key.split(".")
            position = self._data

            for key_level in key_levels:
                # Check the current type, so the type of the last iteration's position isn't
                # checked. This will allow getting non-dict values.
                if type(position) == dict:
                    if key_level in position:
                        # Set position to next dict in "tree"
                        position = position[key_level]
                        continue

                log.write("Error in data_container: Invalid key: %s" % key)
                raise ValueError("Error: Invalid key: %s" % key)

            if not type(position) == list:
                log.write("Error in data_container: Cannot append to %s ( %s ), has to be a list" % type(
                    position), key)
                raise ValueError(
                    "Error: Cannot append to %s ( %s ), has to be a list" % type(position), key)

            position.append(value)

    def pop(self, key, index):
        """Pop the value at an index off a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        with self._lock:
            key_levels = key.split(".")
            position = self._data

            for key_level in key_levels:
                # Check the current type, so the type of the last iteration's position isn't
                # checked. This will allow getting non-dict values.
                if type(position) == dict:
                    if key_level in position:
                        # Set position to next dict in "tree"
                        position = position[key_level]
                        continue

                log.write("Error in data_container: Invalid key: %s" % key)
                raise ValueError("Error: Invalid key: %s" % key)

            if not type(position) == list:
                log.write("Error in data_container: Cannot pop from %s ( %s ), has to be a list" % type(
                    position), key)
                raise ValueError(
                    "Error: Cannot pop from %s ( %s ), has to be a list" % type(position), key)

            position.pop(index)

    def remove(self, key, value):
        """Remove a value from a list responding to a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        with self._lock:
            key_levels = key.split(".")
            position = self._data

            for key_level in key_levels:
                # Check the current type, so the type of the last iteration's position isn't
                # checked. This will allow getting non-dict values.
                if type(position) == dict:
                    if key_level in position:
                        # Set position to next dict in "tree"
                        position = position[key_level]
                        continue

                log.write("Error in data_container: Invalid key: %s" % key)
                raise ValueError("Error: Invalid key: %s" % key)

            if not type(position) == list:
                log.write("Error in data_container: Cannot remove from %s ( %s ), has to be a list" % type(
                    position), key)
                raise ValueError(
                    "Error: Cannot remove from %s ( %s ), has to be a list" % type(position), key)

            position.remove(value)

    def set(self, key, value):
        """Set a value.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        with self._lock:
            key_levels = key.split(".")
            position = self._data

            # Ommit the last key_level from the iteration so position is the dict we want
            # to save the value in.
            for key_level in key_levels[: -1]:
                if type(position) == dict:
                    if key_level in position:
                        # Set position to the nex position
                        position = position[key_level]

                    # Create silently dict if it doesn't exist
                    else:
                        position[key_level] = {}
                        position = position[key_level]

                else:
                    log.write("Error in data_container: Invalid key: %s" % key)
                    raise ValueError("Error: Invalid key: %s" % key)

            # Actually set the value
            position[key_levels[-1]] = value

    def get_data(self):
        """Return a deepcopy of the wrapped data.

        This method is thread safe.
        """

        with self._lock:
            # Always use deepcopy to make it thread safe
            return copy.deepcopy(self._data)

    def get_data_container(self, key):
        """Return a Data_container object representing a dict identified by a key.

        Keys:
            \"user.email\" means root [ "user" ] [ "email" ]

        This method is thread safe.
        """

        # The locking is already being done in self.get
        # Locking here as well would only cause a deadlock
        return Data_container(self.get(key))
