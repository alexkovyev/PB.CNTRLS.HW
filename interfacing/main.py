# coding=utf-8

import time

from InterfacingManager import InterfacingManager
from Message.Message import Message


def test(message):
    print
    "Callback called: ", message


bridge = InterfacingManager("/dev/ttyUSB0", "Node")
bridge.callacks.add("Command", test)
bridge.callacks.add("Command2", test)
# bridge.callacks.add("*", test2)
bridge.start()

try:
    while True:
        msg = Message()
        msg.header.node_name = "Node"
        msg.header.command_name = "Command2"
        msg.parameters.append(84)
        bridge.send(msg)

        time.sleep(2)
except KeyboardInterrupt:
    bridge.join()
