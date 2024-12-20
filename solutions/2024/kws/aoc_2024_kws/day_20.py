import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from collections import Counter, defaultdict

from rich.progress import track, Progress

cardinal_moves = [(0,1), (0,-1), (1,0), (-1,0)]

def dijkstra(grid, start, end=None, cheat_time=0, max_distance=float('inf'), start_grid=None):
    # Initialize distances dictionary with infinity for all points
    if start_grid is None:
        distances = {start: 0}
    else:
        distances = start_grid.copy()

    max_x, max_y = max(x for x, y in grid), max(y for x, y in grid)

    # Priority queue to store (distance, point) tuples
    queue = [(distances[start], start, tuple())]

    # Keep track of visited nodes
    visited = set()
    cheat_path = []

    while queue:
        current_dist, current, cheat_path = min(queue)
        queue.remove((current_dist, current, cheat_path))

        if current == end:
            return distances, cheat_path
        
        if current_dist > max_distance:
            return distances, cheat_path

        if current in visited:
            continue
            
        visited.add(current)

        # Check all four adjacent positions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if next_x <= 0 or next_x >= max_x or next_y <= 0 or next_y >= max_y:
                continue

            if next_pos in visited:
                continue

            cp = list(cheat_path)
            if len(cp) < cheat_time-1:
                pass
            elif next_pos in grid:
                continue

            new_dist = current_dist + 1
            
            # Update distance if shorter path found
            if next_pos not in distances or new_dist < distances[next_pos]:
                distances[next_pos] = new_dist
                if len(cp) < cheat_time:
                    cp.append(next_pos)
                queue.append((new_dist, next_pos, tuple(cp)))
    
    return distances, cheat_path


# def get_all_cheat_grids(grid, start, end):
#     max_x = max(x for x, y in grid)
#     max_y = max(y for x, y in grid)


#     visited_pairs = set()
#     for y in range(max_y + 1):
#         for x in range(max_x + 1):
#             # A valid starting point is not a wall. 
#             if (x, y) not in grid: 
#                 # I can now cheat by removing two wall pieces as long as I can get there within two moves.
#                 # For a total of 12 possible wall removals.
#                 for (dx1, dy1) in cardinal_moves:
#                     x1, y1 = x+dx1, y+dy1
#                     x2, y2 = x1+dx1, y1+dy1
#                     cheat_pair = ((x1, y1), (x2, y2))
#                     if cheat_pair not in visited_pairs and (x1, y1) in grid and (x2, y2) not in grid:
#                         visited_pairs.add(cheat_pair)
#                         yield dijkstra(grid, start, end, ((x,y),(x1,y1))), ((x,y), *cheat_pair)
                    


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day20(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day20.txt").read_text()
        target_saving = 0
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
                

    distances, _ = dijkstra(grid, start)
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
            new_distances, shortcut = dijkstra(grid, (x, y), end, 2, max_distance=target_distance, start_grid=distances)
            saving = end_distance - new_distances.get(end, float('inf'))
            if (x, y) == (9, 7):
                print(new_distances)
                print(f"Shortcut: {shortcut}: {saving}")
            if new_distances.get(end, float('inf')) < end_distance:
                saving = end_distance - new_distances[end]
                counter[saving] += 1
                solutions[saving].append(shortcut)
            progress.update(task, advance=1, description=f"Found {sum(counter.values())} shortcuts.")
            

    # counter = Counter()
    # solutions = defaultdict(list)
    # for new_distance, cheat_pair in get_all_cheat_grids(grid, start, end):
    #     saved = distance - new_distance
    #     if saved > 0:
    #         counter[saved] += 1
    #         solutions[saved].append(cheat_pair)
 
    for time in sorted(counter.keys()):
        print(time, counter[time], solutions[time])

    # more_than_100 = [key for key in counter.keys() if key >= 100]

    # total_saved = sum(counter[key] for key in more_than_100)
    # print(total_saved)

    for cheat_pair in solutions[64]:
        my_grid = grid.copy()
        my_grid[start] = "S"
        my_grid[end] = "E"
        # my_grid[cheat_pair[0]] = "C"
        for ix, coord in enumerate(cheat_pair):
            my_grid[coord] = str(ix+1)
        my_grid[(9,7)] = "X"


        dump_grid(my_grid)

    total_saved = sum(counter.values())
    print(total_saved)


    if not sample:
        submit(total_saved, part="a", day=20, year=2024)



def dump_grid(grid):
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y), "."), end="")
        print()
