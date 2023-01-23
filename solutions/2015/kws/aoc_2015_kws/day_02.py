import click
from aocd import submit

from .cli import main
from .config import config


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day02(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day02.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day02.txt").read_text()

    total = 0
    for line in input_data.splitlines():
        l, w, h = [int(x) for x in line.split("x")]
        sides = [l * w, w * h, h * l]
        total += 2 * sum(sides) + min(sides)

    print("Part 1:", total)

    total = 0
    for line in input_data.splitlines():
        dimensions = sorted([int(x) for x in line.split("x")])
        ribbon = 2 * sum(dimensions[:2]) + dimensions[0] * dimensions[1] * dimensions[2]

        total += ribbon

    print("Part 2:", total)
