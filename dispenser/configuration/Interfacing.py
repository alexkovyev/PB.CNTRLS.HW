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
        msg.parameters.append(str(duration))
        msg.parameters.append(str(size))
        msg.parameters.parameters += [str(x) for x in color]
        self.manager.send(msg)

    def demo_light_mode(self, mode):
        msg = Message()
        msg.header.node_name = Interfacing.device_node_name
        msg.header.command_name = "demo_light_mode"
        msg.parameters.parameters += [int(x) for x in mode.colors]
        msg.parameters.append(mode.min_val)
        msg.parameters.append(mode.max_val)
        msg.parameters.append(mode.min_time)
        msg.parameters.append(mode.rise_time)
        msg.parameters.append(mode.max_time)
        msg.parameters.append(mode.decrease_time)
        msg.parameters.append(mode.max_circles)
        self.manager.send(msg)

    def set_display_image(self, name, duration):
        msg = Message()
        msg.header.node_name = Interfacing.device_node_name
        msg.header.command_name = "set_display_image"
        msg.parameters.append(name)
        msg.parameters.append(duration)

    def set_display_video(self, name, duration):
        msg = Message()
        msg.header.node_name = Interfacing.device_node_name
        msg.header.command_name = "set_display_video"
        msg.parameters.append(name)
        msg.parameters.append(duration)
