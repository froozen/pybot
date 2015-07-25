from data_container import Data_container

_container = Data_container({})


def get(key):
    """Return a value or None if not set

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    return _container.get(key)


def set(key, value):
    """Set a value.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.set(key, value)


def get_data_container(key):
    """Return a Data_container object representing a dict identified by a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    return _container.get_data_container(key)


def append(self, key, value):
    """Append a value to a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.append(key, value)


def pop(self, key, index):
    """Pop the value at an index off a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.pop(key, index)


def remove(self, key, value):
    """Remove a value from a list responding to a key.

    Keys:
        \"user.email\" means root [ "user" ] [ "email" ]

    This method is thread safe.
    """

    # Simply call the method in _container
    _container.remove(key, value)
