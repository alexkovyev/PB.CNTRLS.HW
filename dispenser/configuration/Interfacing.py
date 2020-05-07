from interfacing.Message.Message import Message


class Interfacing(object):
    device_node_name = "Dispenser"

    def __init__(self, manager):
        self.manager = manager

    def ping(self):
        msg = Message()
        msg.header.node_name = Interfacing.device_node_name
        msg.header.command_name = "ping"
        self.manager.send(msg)

    def set_text(self, text, duration, size, color):
        msg = Message()
        msg.header.node_name = Interfacing.device_node_name
        msg.header.command_name = "set_display_text"
        msg.parameters.append(text)
        msg.parameters.append(duration)
        msg.parameters.append(size)
        msg.parameters.parameters += color
        self.manager.send(msg)

