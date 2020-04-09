import Errors
from Message_symbols import message_symbols


class Message_header(object):
    def __init__(self, string=None):
        self.node_name = None
        self.command_name = None

        if string:
            self.string = self.extract(string)
            self.parse()
        else:
            self.string = None

    @staticmethod
    def extract(string):
        start = string.find(message_symbols["header_start_symbol"]) + 1
        end = string.find(message_symbols["header_end_symbol"])
        return string[start:end]

    def parse(self):
        splitted = self.string.split(message_symbols["parameters_splitter"])
        if not splitted[0]:
            raise Errors.MessageFormatError("Header: node name cannot be empty")
        if not splitted[1]:
            raise Errors.MessageFormatError("Header: command cannot be empty")

        self.node_name = splitted[0]
        self.command_name = splitted[1]

    def to_string(self):
        return "{}{}{}".format(self.node_name, message_symbols["parameters_splitter"], self.command_name)

    def __str__(self):
        return "Header: Node: {0}, Command: {1}".format(self.node_name, self.command_name)
