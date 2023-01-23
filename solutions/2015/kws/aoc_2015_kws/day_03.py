import click
from aocd import submit

from .cli import main
from .config import config


def visited_houses(input_data):
    x = y = 0
    visited = {(x, y)}
    for c in input_data:
        if c == ">":
            x += 1
        elif c == "<":
            x -= 1
        elif c == "^":
            y += 1
        elif c == "v":
            y -= 1
        visited.add((x, y))
    return visited


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day03(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day03.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day03.txt").read_text()

    visited = visited_houses(input_data)
    print("Part 1:", len(visited))

    santa1 = visited_houses(input_data[::2])
    santa2 = visited_houses(input_data[1::2])

    print("Part 2:", len(santa1 | santa2))
