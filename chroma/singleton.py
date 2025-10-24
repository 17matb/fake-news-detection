from threading import Lock


class SingletonMeta(type):
    """
    Métaclasse pour implémenter un pattern Singleton.
    Toute classe utilisant cette métaclasse n'aura qu'une seule instance.
    """

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances = instance
        return cls._instances[cls]
