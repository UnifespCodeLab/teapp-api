from flask import request as req


def get_boolean_arg(name, default=True):
    value = req.args.get(name, default=default)
    if value is None:
        return None

    return False if value == 'false' else True


def get_integer_list_arg(name, default=None):
    value = req.args.get(name, None)
    if value is None:
        return default

    return map(int, value.split(','))


def get_string_list_arg(name, default=None):
    value = req.args.get(name, None)
    if value is None:
        return default

    return value.split(',')
