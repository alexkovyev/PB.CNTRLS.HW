import Queue
import thread
import threading

from Callbacks import Callbacks, MessageWrapper
from Message.Errors import MessageFormatError
from Message.Message import Message
from ParametersValidator import ParametersValidator
from SerialBridge import SerialBridge


class InterfacingManager(object):
    def __init__(self, serial_port, node_name):
        self.node_name = node_name

        self.raw_messages_q = Queue.Queue()
        self.messages_q = Queue.Queue()

        self.die = False

        self.bridge = SerialBridge(serial_port, self.raw_messages_q)
        self.bridge.die = self.die

        self.callacks = Callbacks()
        self.validators = ParametersValidator()

    def parser_routine(self):
        try:
            while not self.die:
                if not self.raw_messages_q.empty():
                    raw_msg = self.raw_messages_q.get()
                    try:
                        message = Message(raw_msg)
                        if message.header.node_name == self.node_name:
                            error = self.validators(message)
                            if error:
                                raise MessageFormatError(error)
                            self.messages_q.put(MessageWrapper(message))
                    except MessageFormatError as e:
                        print "An error occurenced while parsing message '{}':\n{}".format(raw_msg, e)
        except KeyboardInterrupt:
            self.stop()
            thread.interrupt_main()

    def callbacks_routine(self):
        try:
            while not self.die:
                if not self.messages_q.empty():
                    message = self.messages_q.get()
                    if not message.processed:
                        self.callacks(message.get())
                    self.messages_q.put(message)
        except KeyboardInterrupt:
            self.stop()
            thread.interrupt_main()

    def start(self):
        self.bridge.start()
        parser_thread = threading.Thread(target=self.parser_routine)
        parser_thread.daemon = True
        callbacks_thread = threading.Thread(target=self.callbacks_routine)
        callbacks_thread.daemon = True
        parser_thread.start()
        callbacks_thread.start()

    def send(self, message):
        message_str = message.to_string()
        self.bridge.send(message_str)
        print "Message sent:", message_str

    def stop(self):
        self.die = True
