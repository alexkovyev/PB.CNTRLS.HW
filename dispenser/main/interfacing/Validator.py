class Validator(object):
    """
    This class stores validation function and range of parameters this function apply to.
    """

    def __init__(self, function, start_id, end_id=None):
        self.function = function
        self.start = start_id
        self.end = end_id

    def __call__(self, parameters):
        end = self.end if self.end else self.start + 1
        if len(parameters) < end:
            return "Not enough parameters: excepted {}, got {}".format(end, len(parameters))

        for param in parameters[self.start:end]:
            error = self.function(param)
            if error:
                return error
