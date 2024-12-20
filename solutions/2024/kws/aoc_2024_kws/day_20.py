import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from collections import Counter, defaultdict

from rich.progress import track, Progress

cardinal_moves = [(0,1), (0,-1), (1,0), (-1,0)]



def dijkstra(grid, start, end=None):
    # Initialize distances dictionary with infinity for all points
    distances = {start: 0}

    # Priority queue to store (distance, point) tuples
    queue = [(distances[start], start)]

    # Keep track of visited nodes
    visited = set()

    while queue:
        current_dist, current = min(queue)
        queue.remove((current_dist, current))

        if current == end:
            return distances
        
        if current in visited:
            continue
            
        visited.add(current)

        # Check all four adjacent positions
        for dx, dy in cardinal_moves:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if next_pos in visited or next_pos in grid:
                continue

            new_dist = current_dist + 1
            
            # Update distance if shorter path found
            if next_pos not in distances or new_dist < distances[next_pos]:
                distances[next_pos] = new_dist
                queue.append((new_dist, next_pos))
    
    return distances


def check_shortcut(grid, start, end, cheat_time, distances):
    x, y = start
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    start_distance = distances[start]

    cheats = []
    for dx in range(-cheat_time, cheat_time+1):
        for dy in range(-cheat_time, cheat_time+1):
            manhattan_distance = abs(dx) + abs(dy)
            if manhattan_distance > cheat_time:
                continue
            current_distance = start_distance + manhattan_distance
            new_x, new_y = x+dx, y+dy
            if distances.get((new_x, new_y), 0) > current_distance:
                saving = distances[(new_x, new_y)] - current_distance
                cheats.append((saving, (x, y),(new_x, new_y)))

    return cheats


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day20(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day20.txt").read_text()
        target_saving = 50
    else:
        input_data = (config.USER_DIR / "day20.txt").read_text()
        target_saving = 100

    grid = {}
    for y, line in enumerate(input_data.splitlines()):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
            elif char == "#":
                grid[(x, y)] = "#"
                

    distances = dijkstra(grid, start)
    end_distance = distances[end]
    print(start, end, end_distance)

    target_distance = end_distance - target_saving    

    # filter grid to find distances where the saving can be 100 or more (i.e. end_distance-102)
    possible_shortcuts = sorted([(k, v) for k, v in distances.items() if v < target_distance], key=lambda x : x[0])
    print("possible shortcuts", len(possible_shortcuts))

    counter = Counter()
    solutions = defaultdict(list)

    with Progress() as progress:
        task = progress.add_task("Checking shortcuts", total=len(possible_shortcuts))
        for (x, y), _ in possible_shortcuts:
            cheats = check_shortcut(grid, (x, y), end, 2, distances=distances)
            for c in cheats:
                saving = c[0]
                if saving >= target_saving:
                    counter[c[0]] += 1
                    solutions[c[0]].append(c[1:])
            progress.update(task, advance=1, description=f"Found {sum(counter.values())} shortcuts.")
            

    for time in sorted(counter.keys()):
        print(time, counter[time], solutions[time])


    total_saved = sum(counter.values())
    print(total_saved)


    if not sample:
        submit(total_saved, part="a", day=20, year=2024)

    counter = Counter()
    solutions = defaultdict(list)


    possible_shortcuts = sorted([(k, v) for k, v in distances.items() if v < target_distance], key=lambda x : x[0])
    print("possible shortcuts", len(possible_shortcuts))

    with Progress() as progress:
        task = progress.add_task("Checking shortcuts", total=len(possible_shortcuts))
        for (x, y), _ in possible_shortcuts:
            cheats = check_shortcut(grid, (x, y), end, 20, distances=distances)
            for c in cheats:
                saving = c[0]
                if saving >= target_saving:
                    counter[c[0]] += 1
                    solutions[c[0]].append(c[1:])
            progress.update(task, advance=1, description=f"Found {sum(counter.values())} shortcuts.")

    for time in sorted(counter.keys()):
        print(time, counter[time])

    total_saved = sum(counter.values())
    print(total_saved)

    if not sample:
        submit(total_saved, part="b", day=20, year=2024)


def dump_grid(grid):
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y), "."), end="")
        print()
