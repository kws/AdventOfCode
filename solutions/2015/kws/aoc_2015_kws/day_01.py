import click
from aocd import submit

from .cli import main
from .config import config


def find_floor(value):
    return value.count("(") - value.count(")")


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day01(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day01.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day01.txt").read_text()

    print("Part 1:", find_floor(input_data))

    current_floor = 0
    for ix, c in enumerate(input_data):
        if c == "(":
            current_floor += 1
        elif c == ")":
            current_floor -= 1

        if current_floor == -1:
            print("Part 2:", ix + 1)
            break
