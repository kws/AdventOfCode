import re
from collections import Counter
from functools import lru_cache
from typing import Dict, Iterable, Iterator, List, Mapping, NamedTuple, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config

PTN_INPUT = re.compile(
    r"^Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


class Valve(NamedTuple):
    name: str
    rate: int


class GraphNode(NamedTuple):
    valve: Valve
    distance: int


class Graph(Mapping[Valve, Tuple[GraphNode]]):
    def __init__(self, graph: Mapping[Valve, Iterable[GraphNode]]):
        self._graph = [
            (k, tuple(v1 for v1 in sorted(v, key=lambda v1: v1.valve.name)))
            for k, v in graph.items()
        ]
        self._graph = tuple(sorted(self._graph, key=lambda v: v[0].name))

    @lru_cache
    def __getitem__(self, item: Valve) -> Tuple[GraphNode]:
        return next(v[1] for v in self._graph if v[0] == item)

    def __iter__(self) -> Iterator[Valve]:
        return iter([item[0] for item in self._graph])

    def __len__(self) -> int:
        return len(self._graph)

    def __hash__(self):
        return hash(self._graph)

    def __eq__(self, other):
        return self._graph == other._graph


class ValveRegistry(Mapping[str, Valve]):
    def __init__(self, input: str):
        valves_by_name = {}
        links_by_name = {}
        for line in input.splitlines():
            match = PTN_INPUT.match(line)
            if not match:
                raise ValueError(f"Invalid valve config: {line}")
            name, flow_rate, links = match.groups()
            valves_by_name[name] = Valve(name, int(flow_rate))
            links_by_name[name] = [l.strip() for l in links.split(",")]

        valves = {}
        for valve in valves_by_name.values():
            valves[valve] = [
                GraphNode(valves_by_name[link], 1) for link in links_by_name[valve.name]
            ]

        self.__graph = Graph(valves)
        self.__valves = valves_by_name

    @property
    def graph(self) -> Graph:
        return self.__graph

    def __getitem__(self, item: str) -> Valve:
        return self.__valves[item]

    def __getattr__(self, item) -> Valve:
        return self.__valves[item]

    def __len__(self) -> int:
        return len(self.__valves)

    def __iter__(self) -> Iterator[Valve]:
        return iter(self.__valves.values())


@lru_cache
def dijkstra(graph: Graph, source: Valve) -> Dict[Valve, int]:
    distances = {valve: float("inf") for valve in graph}
    distances[source] = 0
    unvisited = set(graph)

    # Repeat until all vertices are visited
    while unvisited:
        # Select the unvisited vertex with the smallest distance
        current = min(unvisited, key=lambda vertex: distances[vertex])

        # Update distances of neighbors
        for node in graph[current]:
            if node.valve in unvisited:
                distances[node.valve] = min(
                    distances[node.valve], distances[current] + node.distance
                )

        # Remove current from unvisited
        unvisited.remove(current)

    return distances


def simplify_graph(
    graph: Graph, opened_valves: Iterable[Valve], keep: Valve = None
) -> Graph:
    to_remove = set(v for v in graph if v.rate == 0 or v in opened_valves)
    if keep:
        to_remove -= {keep}

    if not to_remove:
        return graph

    graph = dict(graph)

    # For each node to remove, find all nodes that link to that node, and link to the removed node's neighbours instead
    # repeat until no more nodes to remove
    while to_remove:
        node = to_remove.pop()
        for n in graph:
            if node in [g.valve for g in graph[n]]:
                # Find the distance to the node
                node_distance = next(g.distance for g in graph[n] if g.valve == node)

                # New neighbours are the existing neighbours except the node to remove
                new_neighbours = [GraphNode(v, d) for v, d in graph[n] if v != node]

                # Add the neighbours of the node to remove except links to the node itself
                new_neighbours.extend(
                    [GraphNode(v, d + node_distance) for v, d in graph[node] if v != n]
                )

                graph[n] = new_neighbours

        del graph[node]

    return Graph(graph)


def find_path(
    graph: Graph, start_node: Valve, time_left, opened_nodes=None, player_2=False
) -> List[List[GraphNode]]:
    if opened_nodes is None:
        opened_nodes = set()

    to_open = set(n for n in graph if n.rate > 0) - opened_nodes

    if not to_open:
        return [[GraphNode(start_node, time_left)]]

    distances = dijkstra(graph, start_node)

    paths = [[GraphNode(start_node, time_left)]]
    graph = simplify_graph(graph, opened_nodes)
    while to_open:
        valve = to_open.pop()
        time = time_left - distances[valve] - 1
        if time > 0:
            for p in find_path(graph, valve, time, opened_nodes | {valve}, player_2):
                if player_2 and to_open:
                    for valve_2 in to_open:
                        for p2 in find_path(
                            graph, valve, time, opened_nodes | {valve, valve_2}
                        ):
                            if (
                                set(n.valve for n in p2[1:]).union(
                                    n.valve for n in p[1:]
                                )
                                == {}
                            ):
                                paths.append(
                                    [GraphNode(start_node, time_left)] + p + p2
                                )
                else:
                    paths.append([GraphNode(start_node, time_left)] + p)

    return paths


def score_paths(paths):
    for p in paths:
        output = sum(v.rate * t for v, t in p)
        summary = "/".join(f"{v.name}[{v.rate * t}]" for v, t in p)
        yield output, summary


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day16(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day16.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day16.txt").read_text()

    valve_registry = ValveRegistry(input_data)
    AA = valve_registry.AA
    graph = simplify_graph(valve_registry.graph, {}, keep=AA)

    paths = find_path(graph, AA, 30)
    paths = sorted(score_paths(paths))

    for p in paths[-10:]:
        print(p)

    paths = find_path(graph, AA, 30, player_2=True)
    paths = sorted(score_paths(paths))

    for p in paths[-10:]:
        print(p)