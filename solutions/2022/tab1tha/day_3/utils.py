import pandas as pd
import string

lowercase = list(string.ascii_lowercase)
small_weights = list(range(1, 27))
small_priorities = dict(zip(lowercase, small_weights))

uppercase = list(string.ascii_uppercase)
upper_weights = list(range(27, 53))
upper_priorities = dict(zip(uppercase, upper_weights))

priorities_map = small_priorities | upper_priorities


def string_in_two(strng):
    """divide a string into two equal parts"""
    first_part = strng[: len(strng) // 2]
    second_part = strng[len(strng) // 2 :]
    return [first_part, second_part]


def common_element(first_part, second_part):
    # find element types that exist in both compartments.
    unique_firsts = set(list(first_part))
    unique_seconds = set(list(second_part))
    # set unpacking. Assumes that there is always only one common element.
    try:
        commoner, *_ = unique_firsts.intersection(unique_seconds)
    except:
        commoner = pd.NA
    # use list(set) and explode the dataframe to account for multiple commoners

    return commoner
