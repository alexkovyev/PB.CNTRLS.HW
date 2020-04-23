from Message_symbols import message_symbols


class MessageParameters(object):
    def __init__(self, string=None):
        self.parameters = []
        if string:
            self.string = self.extract(string)
            self.parse()
        else:
            self.string = None

    @staticmethod
    def extract(string):
        start = string.find(message_symbols["parameters_start_symbol"]) + 1
        end = string.find(message_symbols["parameters_end_symbol"])
        return string[start:end]

    def parse(self):
        self.parameters = self.string.split(message_symbols["parameters_splitter"])

    def to_string(self):
        return message_symbols["parameters_splitter"].join(str(x) for x in self.parameters)

    def append(self, param):
        self.parameters.append(param)

    def __getitem__(self, index):
        return self.parameters[index]

    def __setitem__(self, index, value):
        self.parameters[index] = value

    def __delitem__(self, index):
        del self.parameters[index]

    def __str__(self):
        return "Parameters: " + ", ".join(self.parameters)
