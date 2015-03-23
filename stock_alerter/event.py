class Event:
    """A generic class that provides signal/slot functionality"""

    def __init__(self):
        self.listeners = []

    def connect(self, listener):
        self.listeners.append(listener)

    def fire(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)
