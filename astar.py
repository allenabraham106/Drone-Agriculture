import heapq
# 1 = Wall
# 0 = Open space
grid = [
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
]

# print the whole grind
for row in grid:
    print(row)

start = (0, 3)
goal = (4, 4)

# based on values set above
print(f"Start: {start}")
print(f"Goal: {goal}")


# movement handeler
def get_neighbors(pos, grid):
    row, col = pos
    move = [
        (0, 1),  # right
        (0, -1),  # left
        (1, 0),  # down
        (-1, 0),  # up
    ]
    neighbors = []

    # move in every direction and keep track of neighbors
    for row_change, col_change in move:
        new_row = row + row_change
        new_col = col + col_change
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            print(new_row, new_col, grid[new_row][new_col])
            if grid[new_row][new_col] == 0:
                neighbors.append((new_row, new_col))
    return neighbors


def heuristic(current, goal):
    # how far apart are the rows and how far apart is our location on the rows
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


#its been a minute since wokring. 
# Adding temporary comments to understand
def astar(grid, goal, start):
    come_from = {
        #how did we get everywhere 
    }
    open_list = [
        #we know it exists just haven't explored
    ]
    g_score = {
        #travel cost for a position
        start : 0
    }
    heapq.heappush(open_list, (0, start))


print(get_neighbors(start, grid))
print(heuristic(start, goal))
