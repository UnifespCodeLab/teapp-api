def get_update_dict(include, data) -> dict:
    verified = {}
    for key in data:
        if key in include:
            verified[key] = data[key]

    if len(verified) == 0:
        return None

    return verified
