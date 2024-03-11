"""Module defining the task functions available for execution."""


def sum_numbers(a: float, b: float) -> float:
    """Returns the sum of two numbers.

    Args:
        a (float): The first number to add.
        b (float): The second number to add.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b


def concat_strings(str1: str, str2: str, str3: str) -> str:
    """Concatenates three strings.

    Args:
        str1 (str): The first string to concatenate.
        str2 (str): The second string to concatenate.
        str3 (str): The third string to concatenate.

    Returns:
        str: The concatenated string.
    """
    return str1 + str2 + str3


def multiply_numbers(a: float, b: float) -> float:
    """Returns the product of two numbers.

    Args:
        a (float): The first number to multiply.
        b (float): The second number to multiply.

    Returns:
        float: The product of the two numbers.
    """
    return a * b

