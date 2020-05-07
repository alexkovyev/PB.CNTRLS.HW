from InterfacingManager import InterfacingManager
from Validator import Validator


def test(message):
    print "Callback called: ", message


def validation_fn(param):
    try:
        int(param)
    except ValueError:
        return "Parameter should be integer"


interfacing = InterfacingManager("", "Node")
interfacing.callacks.add("Command", test)
interfacing.callacks.add("Command2", test)
# bridge.callacks.add("*", test2)


test_validator = Validator(validation_fn, 0)
interfacing.validators.add("Command3", test_validator)

interfacing.start()

valid_message = "#[Node;Command](42, hello)#"
interfacing.raw_messages_q.put(valid_message)

invalid_format_messages = [
    "#[Node;Command](42, hello)", "[Node;Command](42, hello)#",
    "#[Node;Command(42, hello)#", "#[NodeCommand](42, hello)#",
    "#[Node;Command]42, hello)#", "#[;Command](42, hello)#"
]

for msg in invalid_format_messages:
    interfacing.raw_messages_q.put(msg)

valid_parameters_message = "#[Node;Command3](42)#"
interfacing.raw_messages_q.put(valid_parameters_message)

invalid_parameters_message = "#[Node;Command3](hello)#"
interfacing.raw_messages_q.put(invalid_parameters_message)

try:
    while True:
        pass
except KeyboardInterrupt:
    interfacing.stop()
