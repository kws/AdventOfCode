from enum import Enum

import numpy as np
import re
import click
from aocd import submit

from .cli import main
from .config import config

input_re = re.compile("(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")

@main.command()
@click.option("--sample", "-s", is_flag=True)
def day06(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day06.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day06.txt").read_text()

    lights = np.zeros((1000, 1000), dtype=int)
    for line in input_data.splitlines():
        match = input_re.match(line.strip())
        if match:
            action, x1, y1, x2, y2 = match.groups()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if action == "turn on":
                lights[x1:x2+1, y1:y2+1] = 1
            elif action == "turn off":
                lights[x1:x2+1, y1:y2+1] = 0
            elif action == "toggle":
                lights[x1:x2+1, y1:y2+1] = lights[x1:x2+1, y1:y2+1] ^ 1
        else:
            raise ValueError(f"Invalid action: '{line}'")
        print(line, lights.sum())

    print(lights.sum())

    lights = np.zeros((1000, 1000), dtype=int)
    for line in input_data.splitlines():
        match = input_re.match(line.strip())
        if match:
            action, x1, y1, x2, y2 = match.groups()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if action == "turn on":
                lights[x1:x2+1, y1:y2+1] += 1
            elif action == "turn off":
                lights[x1:x2+1, y1:y2+1] = np.maximum(lights[x1:x2+1, y1:y2+1] - 1, 0)
            elif action == "toggle":
                lights[x1:x2+1, y1:y2+1] += 2
        else:
            raise ValueError(f"Invalid action: '{line}'")
        print(line, lights.sum())

    print(lights.sum())
