import json
import logging


def get_unit_value_from_string(value: str, unit_multiplier_map: dict) -> int:
    """
    Get the value from a string

    Ex. 1.5k -> 1500
        2min -> 120
    :param value: The value
    :param unit_multiplier_map: The unit multiplier map
    :return: The value
    """

    unit = ""
    for char in reversed(value):
        if not char.isnumeric():
            unit = char + unit
        else:
            break

    value_str = value.strip().replace(",", "").replace(".", "").replace(unit, "")

    # Amount not numeric
    if not value_str.isnumeric():
        raise ValueError

    if unit == "":
        return int(value_str)

    # Set magnitude full name
    for key in unit_multiplier_map:
        # There is a key that is a substring of the magnitude, e.g. 'sec' is a substring of
        # 'seconds' (starts with)
        if key.startswith(unit.lower()):
            unit_full_name = key
            break
    else:
        raise ValueError

    # Replace "," with "." to allow float conversion
    value_str = value.replace(",", ".").replace(unit, "")

    # More than 1 decimal point
    if value_str.count(".") > 1:
        raise ValueError

    return int(float(value_str) * unit_multiplier_map[unit_full_name])


def object_to_json_string(obj: any) -> str:
    """
    Convert an object to a JSON string
    :param obj: The object
    :return: The JSON string
    """
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, separators=(",", ":"))


def get_belly_formatted(belly: int) -> str:
    """
    Returns a formatted string of the belly
    :param belly: The belly to format e.g. 1000000
    :return: The formatted belly e.g. 1,000,000
    """
    if belly is None:
        logging.info("Get belly formatted with belly None, returning 0")
        return "0"

    return "{0:,}".format(int(belly))
