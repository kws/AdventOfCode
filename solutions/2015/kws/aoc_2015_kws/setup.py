from pathlib import Path

import click
import yaml
from aocd import get_data
from dateutil.utils import today

from .cli import main
from .config import config

with open(Path(__file__).parent / "setup_templates.yaml") as f:
    templates = yaml.safe_load(f)


def __create_main_file(day):
    filename = Path(__file__).parent / f"day_{day}.py"
    if filename.exists():
        click.echo(f"Day {day} already exists")
    else:
        filename.parent.mkdir(exist_ok=True, parents=True)
        filename.write_text(templates["main"].format(day=day))


def __create_sample_file(day):
    sample_file = config.SAMPLE_DIR / f"day{day}.txt"
    if not sample_file.exists():
        sample_file.parent.mkdir(exist_ok=True, parents=True)
        sample_file.touch()


def __create_data_file(day):
    data_file = config.USER_DIR / f"day{day}.txt"
    if not data_file.exists():
        data = get_data(day=int(day), year=config.AOC_EVENT)
        data_file.parent.mkdir(exist_ok=True, parents=True)
        data_file.write_text(data)


def __create_test_file(day):
    test_file = config.TESTS_DIR / f"test_day{day}.py"
    if not test_file.exists():
        test_file.parent.mkdir(exist_ok=True, parents=True)
        test_file.write_text(
            templates["test_file"].format(day=day, package=config.PACKAGE_NAME)
        )


@main.command()
@click.argument("day", type=int, default=today().day)
def create(day):
    """Create a new day"""
    day = str(day).zfill(2)
    __create_main_file(day)
    __create_sample_file(day)
    __create_data_file(day)
    __create_test_file(day)
