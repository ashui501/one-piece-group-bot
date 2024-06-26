import random


def get_value_from_percentage(total: float, percentage: float) -> float:
    """
    Gets a value from a percentage
    :param total: The value to get the percentage from
    :param percentage: The percentage to get the value from
    :return: The value from the percentage
    """

    return (total * percentage) / 100


def get_random_win(percentage: float) -> bool:
    """
    Gets a random win based on the percentage
    :param percentage: The percentage to get a win for
    :return: True if the percentage is greater than a random number, False otherwise
    """
    return percentage * 10000 >= random.randint(0, 1000000)


def get_random_int(min_value: int, max_value: int) -> int:
    """
    Gets a random int between the min and max values
    :param min_value: The minimum value
    :param max_value: The maximum value
    :return: The random int
    """

    return random.randint(min_value, max_value)


def get_random_key_based_on_probability(probability_dict: dict[any, float]) -> any:
    """
    This function returns a random key from a dictionary based on the probability associated with
    each key.
    The input dictionary, 'probability_dict', should have keys of any type and values of type
    float, representing the probability associated with each key.

    :param probability_dict: The dictionary containing keys and their associated probabilities
    :return: A random key from the dictionary based on the associated probabilities
    """

    # Calculate the total sum of all probability values in the dictionary
    total_probability = sum(probability_dict.values())

    # Generate a random integer within the range of 0 to total_probability - 1
    random_number = get_random_int(1, total_probability)

    # Initialize a variable to accumulate the sum of probabilities
    accumulated_probability = 0

    # Iterate over each key-value pair in the dictionary
    for key, probability in probability_dict.items():
        # Add the current probability to the accumulated sum
        accumulated_probability += probability

        # If the accumulated sum is greater than the random number, return the current key
        if accumulated_probability > random_number:
            return key

    # If no key is found that satisfies the condition, return the last key from the dictionary
    return list(probability_dict.keys())[-1]


def get_percentage_from_value(value: float, total: float, add_decimal=True) -> float:
    """
    Gets a percentage from a value
    :param value: The value to get the percentage from
    :param total: The total value
    :param add_decimal: True if the percentage should have a decimals, False otherwise
    :return: The percentage from the value
    """

    try:
        result = (value / total) * 100
        if not add_decimal:
            return int(result)

        return result
    except ZeroDivisionError:
        return 0


def get_interest_percentage_from_value(value: float, total: float, add_decimal=True) -> float:
    """
    Gets a percentage from a value
    :param value: The value to get the percentage from
    :param total: The total value
    :param add_decimal: True if the percentage should have a decimals, False otherwise
    :return: The percentage from the value
    """

    return get_percentage_from_value(value, total, add_decimal) - 100


def add_percentage_to_value(value: float, percentage: float) -> float:
    """
    Adds a percentage to a value
    :param value: The value to add the percentage to
    :param percentage: The percentage to add to the value
    :return: The value with the percentage added
    """

    if percentage is None or percentage == 0:
        return value

    return value + get_value_from_percentage(value, percentage)


def subtract_percentage_from_value(value: float, percentage: float) -> float:
    """
    Subtracts a percentage from a value
    :param value: The value to subtract the percentage from
    :param percentage: The percentage to subtract from the value
    :return: The value with the percentage subtracted
    """

    return value - get_value_from_percentage(value, percentage)


def get_cumulative_percentage_sum(percentages: list[float]) -> float:
    """
    Calculate the cumulative sum of percentages.
    This function takes a list of percentages and calculates the cumulative sum by iteratively
    adding each percentage to the result and adjusting the remaining percentage for subsequent
    iterations.
    :param percentages: A list of percentages to sum.
    :return: The cumulative sum of the percentages.
    """
    result = 0
    remaining_percentage = 100

    for percentage in percentages:
        # Calculate the percentage of the remaining percentage
        percentage_of_remaining_percentage = (remaining_percentage * percentage) / 100
        result += percentage_of_remaining_percentage
        remaining_percentage -= percentage_of_remaining_percentage

    return result


def format_percentage_value(percentage: float, decimals: int = 2) -> int | float:
    """
    Convert a percentage to an integer value or a float value with specified decimals.

    :param percentage: The percentage to convert.
    :param decimals: Number of decimal places (default is 2).
    :return: An integer or float value.
    """

    if percentage % 1 == 0:
        return int(percentage)

    return round(percentage, decimals)
