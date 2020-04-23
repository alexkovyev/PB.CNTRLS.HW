import Errors
from MessageHeader import MessageHeader
from MessageParameters import MessageParameters
from Message_symbols import message_symbols


class Message(object):
    def __init__(self, string=None):
        self.string = string

        if string:
            error = self.check()
            if error:
                raise Errors.MessageFormatError(error)

            self.header = MessageHeader(string)
            self.parameters = MessageParameters(string)
        else:
            self.header = MessageHeader()
            self.parameters = MessageParameters()

    def check(self):
        # a bit dirty, but i don`t want to use regex
        if self.string[0] != message_symbols["start_symbol"]:
            return "Message should start with " + message_symbols["start_symbol"]
        if self.string[-1:] != message_symbols["end_symbol"]:
            return "Message should end with " + message_symbols["end_symbol"]
        if self.string.count(message_symbols["header_start_symbol"]) != 1:
            return "Message should contain 1 " + message_symbols["header_start_symbol"]
        if self.string.count(message_symbols["header_end_symbol"]) != 1:
            return "Message should contain 1 " + message_symbols["header_end_symbol"]
        if self.string.count(message_symbols["parameters_start_symbol"]) != 1:
            return "Message should contain 1 " + message_symbols["parameters_start_symbol"]
        if self.string.count(message_symbols["parameters_end_symbol"]) != 1:
            return "Message should contain 1 " + message_symbols["parameters_end_symbol"]
        if self.string.count(message_symbols["parameters_splitter"]) < 1:
            return "Message should contain at least 1 " + message_symbols["parameters_splitter"]
        return ""

    def to_string(self):
        header_str = self.header.to_string()
        parameters_str = self.parameters.to_string()
        header_str = "{}{}{}".format(message_symbols["header_start_symbol"], header_str,
                                     message_symbols["header_end_symbol"])
        parameters_str = "{}{}{}".format(message_symbols["parameters_start_symbol"], parameters_str,
                                         message_symbols["parameters_end_symbol"])
        return "{}{}{}{}".format(message_symbols["start_symbol"], header_str, parameters_str,
                                 message_symbols["end_symbol"])

    def __str__(self):
        res = "Message: {\n"
        res += "\t" + self.header.__str__() + "\n"
        res += "\t" + self.parameters.__str__() + "\n"
        res += "}"
        return res
