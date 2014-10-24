def locked ( lock ):
    def locked_decorator ( method ):
        def locked_method ( *args, **kwargs ):
            with lock:
                return method ( *args, **kwargs )

        return locked_method
    return locked_decorator
