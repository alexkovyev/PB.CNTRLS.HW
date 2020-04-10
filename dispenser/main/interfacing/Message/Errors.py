class MessageFormatError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return "Message format error: {0}".format(self.message)
        else:
            return "Message has incorrect format!"
