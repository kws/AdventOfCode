import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit

#         Each obsidian robot produces 1 obsidian per minute and takes 1 minute to build and costs 3 ore and 14 clay.
#         Each geode robot produces 1 geode per minute and takes 1 minute to build and costs 2 ore and 7 obsidian.


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day19(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day19.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day19.txt").read_text()

    # submit(my_answer, part="a", day=19, year=2022)
    maximise()
