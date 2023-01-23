from enum import Enum

import click
from aocd import submit

from .cli import main
from .config import config


class Child(Enum):
    NICE = "Nice"
    NAUGHTY = "Naughty"


naughty_strings = ["ab", "cd", "pq", "xy"]


def has_naughty_string(line):
    return any(s in line for s in naughty_strings)


def has_three_vowels(line):
    return sum(line.count(c) for c in "aeiou") >= 3


def has_repeating_letter(line):
    return any(line[ix] == line[ix + 1] for ix in range(len(line) - 1))


def has_repeating_pair(line):
    for ix in range(len(line) - 1):
        if line[ix : ix + 2] in line[ix + 2 :]:
            return True
    return False


def has_repeating_letter_with_gap(line):
    for ix in range(len(line) - 2):
        if line[ix] == line[ix + 2]:
            return True
    return False


def nice_or_naughty(line):
    if has_naughty_string(line):
        return Child.NAUGHTY
    if not has_three_vowels(line):
        return Child.NAUGHTY
    if not has_repeating_letter(line):
        return Child.NAUGHTY
    return Child.NICE


def nice_or_naughty2(line):
    if not has_repeating_pair(line):
        return Child.NAUGHTY
    if not has_repeating_letter_with_gap(line):
        return Child.NAUGHTY
    return Child.NICE


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day05(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day05.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day05.txt").read_text()

    results = [nice_or_naughty(line) for line in input_data.splitlines()]
    print("Part 1:", results.count(Child.NICE))

    results = [nice_or_naughty2(line) for line in input_data.splitlines()]
    print("Part 2:", results.count(Child.NICE))
