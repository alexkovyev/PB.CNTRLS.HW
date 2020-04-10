def is_int(param):
    try:
        int(param)
    except ValueError:
        return "Parameter should be integer"


def is_float(param):
    try:
        float(param)
    except ValueError:
        return "Parameter should be float"


def is_positive(param):
    if float(param) < 0:
        return "Parameter cannot be negative"


def is_positive_int(param):
    error = is_int(param)
    if error:
        return error
    error = is_positive(param)
    if error:
        return error


def check_str(param):
    if len(param) == 0:
        return "Parameter cannot be empty"


def check_bool(param):
    if param not in ["0", "1"]:
        return "Bolean parameters can only be 0 or 1"


def check_color_val(param):
    error = is_int(param)
    if error:
        return error
    error = is_positive(param)
    if error:
        return error

    int_param = int(param)
    if int_param < 0 or int_param > 255:
        return "Color values can only be in range 0-255"


def check_seconds(param):
    error = is_float(param)
    if error:
        return error
    error = is_positive(param)
    if error:
        return error
