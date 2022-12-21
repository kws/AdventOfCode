from collections import defaultdict, deque
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple, TypeAlias

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.progress import Progress


class Resource(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


Amount: TypeAlias = int


# The current number of robots
class Robots(NamedTuple):
    ore: Amount = 1
    clay: Amount = 0
    obsidian: Amount = 0
    geode: Amount = 0

    def update(self, robot: Resource, amount=1) -> "Robots":
        robot_count = [self[i] for i in range(len(self))]
        robot_count[robot] += amount
        return Robots(*robot_count)


class RobotCost(NamedTuple):
    ore: Amount = 0
    clay: Amount = 0
    obsidian: Amount = 0
    geode: Amount = 0


class ResourceStore(NamedTuple):
    ore: Amount = 0
    clay: Amount = 0
    obsidian: Amount = 0
    geode: Amount = 0

    def increment(self, robots: Robots) -> "ResourceStore":
        return ResourceStore(
            ore=self.ore + robots.ore,
            clay=self.clay + robots.clay,
            obsidian=self.obsidian + robots.obsidian,
            geode=self.geode + robots.geode,
        )

    def subtract(self, costs: RobotCost):
        return ResourceStore(
            ore=self.ore - costs.ore,
            clay=self.clay - costs.clay,
            obsidian=self.obsidian - costs.obsidian,
            geode=self.geode - costs.geode,
        )


class Blueprint(NamedTuple):
    ore: RobotCost
    clay: RobotCost
    obsidian: RobotCost
    geode: RobotCost

    def can_afford(self, store: ResourceStore, robot: Resource) -> bool:
        costs = self[robot]
        can_afford = [s[0] >= s[1] for s in zip(store, costs)]
        return all(can_afford)


@dataclass(frozen=True)
class FactoryState:
    blueprint: Blueprint
    time_left: int = 24
    robots: Robots = Robots()
    resources: ResourceStore = ResourceStore()

    @property
    def potential(self) -> int:
        return (
            self.resources.geode
            + self.robots.geode * self.time_left
            + (self.time_left * (self.time_left - 1) // 2)
        )

    def next_states(self) -> tuple["FactoryState"]:
        next_resources = self.resources.increment(self.robots)

        # Outta time...
        if self.time_left == 0:
            return

        # Doing nothing is always possible
        yield FactoryState(
            blueprint=self.blueprint,
            time_left=self.time_left - 1,
            robots=self.robots,
            resources=next_resources,
        )

        # Can we make a robot?
        for r in Resource:
            if self.blueprint.can_afford(self.resources, r):
                new_robots = self.robots.update(r)
                yield FactoryState(
                    blueprint=self.blueprint,
                    time_left=self.time_left - 1,
                    robots=new_robots,
                    resources=next_resources.subtract(self.blueprint[r]),
                )


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day19(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day19.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day19.txt").read_text()

    sample_blueprint = Blueprint(
        RobotCost(ore=4),
        RobotCost(ore=2),
        RobotCost(ore=3, clay=14),
        RobotCost(ore=2, obsidian=7),
    )

    start_state = FactoryState(blueprint=sample_blueprint)
    states = deque([start_state])
    all_states = []

    with Progress() as progress:
        task1 = progress.add_task("[red]Calculating...", total=None)

        max_potential = defaultdict(int)
        rejected = 0
        while states:
            progress.update(
                task1,
                description=f"{len(all_states)} states / {len(states)} in queue / {rejected} rejected",
            )
            state = states.pop()
            if state.potential >= max_potential[state.time_left]:
                states.extend(state.next_states())
                max_potential[state.time_left] = state.potential
            else:
                rejected += 1

            if state.time_left == 0:
                all_states.append(state)

    all_states.sort(key=lambda s: s.resources.geode, reverse=True)
    for state in all_states:
        print(state.resources)
