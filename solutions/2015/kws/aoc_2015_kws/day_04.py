import hashlib

import click
from tqdm import trange

from .cli import main
from .config import config


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day04(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day04.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day04.txt").read_text()

    for i in trange(10000000):
        if hashlib.md5((input_data + str(i)).encode()).hexdigest().startswith("00000"):
            break

    part1 = i
    print("Part 1:", part1)

    for i in trange(part1, 10000000):
        if hashlib.md5((input_data + str(i)).encode()).hexdigest().startswith("000000"):
            break

    print("Part 2:", i)
