"""Thread-safe singleton with the interface required by the task."""
from threading import Lock


class Singleton:
    """Share a single settings object through construction and getInstance."""
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls is not Singleton:
            raise TypeError("Subclassing is disabled for this singleton")
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.station = "Observatory North"
        return cls._instance

    @classmethod
    def getInstance(cls):
        """Keep the exact method spelling requested by the assignment."""
        return cls()

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (Singleton, ())

    def printInfo(self):
        """Display the shared station label."""
        print(self.station)


if __name__ == "__main__":
    Singleton.getInstance().printInfo()
