class Event_Hook:

    handlers = []

    def __init__(self):
        self.handlers = []

    def register(self, handler):
        self.handlers.append(handler)
        return self
    
    def unregister(self, handler):
        self.handlers.remove(handler)
        return self
    
    def trigger(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)