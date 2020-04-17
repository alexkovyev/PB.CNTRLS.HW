import threading


class Callbacks(object):
    def __init__(self):
        self.callbacks = {}

    def add(self, command_name, function):
        if command_name not in self.callbacks:
            self.callbacks[command_name] = []

        self.callbacks[command_name].append(function)

    def __call__(self, message, run_async=False):
        if message.header.command_name not in self.callbacks and "*" not in self.callbacks:
            return False

        callbacks = self.callbacks[message.header.command_name]
        # The * sign indicates that the callback should be called for every command
        if "*" in self.callbacks:
            callbacks += self.callbacks["*"]
        for callback in callbacks:
            if run_async:
                thread = threading.Thread(target=callback, args=(message,))
                thread.daemon = True
                thread.run()
            else:
                callback(message)

        return True


class MessageWrapper(object):
    def __init__(self, message):
        self._message = message

        self.processed = False

    def get(self):
        self.processed = True
        return self._message
