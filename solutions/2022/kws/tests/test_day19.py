import pytest
from aoc_2022_kws.day_19 import (
    Blueprint,
    FactoryState,
    Resource,
    ResourceStore,
    RobotCost,
    Robots,
)


@pytest.fixture
def sample_blueprint():
    return Blueprint(
        RobotCost(ore=4),
        RobotCost(ore=2),
        RobotCost(ore=3, clay=14),
        RobotCost(ore=2, obsidian=7),
    )


def test_robots():
    my_robots = Robots()
    assert my_robots.ore == 1
    assert sum(my_robots) == 1

    my_robots = my_robots.update(Resource.ORE)
    assert my_robots.ore == 2
    assert sum(my_robots) == 2

    my_robots = my_robots.update(Resource.CLAY)
    assert my_robots.ore == 2
    assert my_robots.clay == 1
    assert sum(my_robots) == 3


def test_affordability(sample_blueprint):
    my_store = ResourceStore(ore=2)
    assert not sample_blueprint.can_afford(my_store, Resource.ORE)
    assert sample_blueprint.can_afford(my_store, Resource.CLAY)
    assert not sample_blueprint.can_afford(my_store, Resource.OBSIDIAN)
    assert not sample_blueprint.can_afford(my_store, Resource.GEODE)

    my_store = ResourceStore(ore=4)
    assert sample_blueprint.can_afford(my_store, Resource.ORE)
    assert sample_blueprint.can_afford(my_store, Resource.CLAY)
    assert not sample_blueprint.can_afford(my_store, Resource.OBSIDIAN)
    assert not sample_blueprint.can_afford(my_store, Resource.GEODE)

    my_store = ResourceStore(ore=3, clay=14)
    assert not sample_blueprint.can_afford(my_store, Resource.ORE)
    assert sample_blueprint.can_afford(my_store, Resource.CLAY)
    assert sample_blueprint.can_afford(my_store, Resource.OBSIDIAN)
    assert not sample_blueprint.can_afford(my_store, Resource.GEODE)


def test_next_states(sample_blueprint):
    start_state = FactoryState(blueprint=sample_blueprint)
    states = list(start_state.next_states())

    assert len(states) == 1

    assert states[0].robots.ore == 1
    assert states[0].resources.ore == 1

    states = list(states[0].next_states())

    assert len(states) == 1
    assert states[0].robots.ore == 1
    assert states[0].resources.ore == 2

    states = list(states[0].next_states())

    assert len(states) == 2
    assert states[0].robots.ore == 1
    assert states[0].robots.clay == 0
    assert states[0].resources.ore == 3

    assert states[1].robots.ore == 1
    assert states[1].robots.clay == 1
    assert states[1].resources.ore == 1
