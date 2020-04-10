class ParametersValidator(object):
    def __init__(self):
        self.validators = {}

    def add(self, command_name, validator):
        if command_name not in self.validators:
            self.validators[command_name] = []

        if isinstance(validator, list):
            self.validators[command_name] += validator
        else:
            self.validators[command_name].append(validator)

    def __call__(self, message):
        if message.header.command_name not in self.validators and "*" not in self.validators:
            return None

        validators = self.validators[message.header.command_name]
        if "*" in self.validators:
            validators += self.validators["*"]

        for validator in validators:
            error = validator(message.parameters.parameters)
            if error:
                range_str = str(validator.start) if not validator.end else "({}:{})".format(validator.start,
                                                                                            validator.end)
                return "Invalid parameters {}: {}".format(range_str, error)
        return None
