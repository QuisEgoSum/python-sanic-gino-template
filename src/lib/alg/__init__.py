def merge_dict_priority(low, high, simple=True) -> dict:
    result = dict()
    for key, value in low.items():
        if key not in high:
            result[key] = value
            continue
        if type(value) == dict:
            result[key] = merge_dict_priority(value, high[key], simple)
        elif key in high:
            result[key] = high[key]
        else:
            result[key] = value
    if simple is False:
        for key, value in high.items():
            if key not in low:
                result[key] = value
            elif type(value) == dict:
                result[key] = merge_dict_priority(low[key], value, simple)
            else:
                result[key] = value
    return result

