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


# where can I move
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
    heapq.heappush(open_list, (0, start))  #zero cause you haven't gone anywhere yet

    # so it basically find the lowest f score fromt he list of places we know exists, 
    # if they are the goal then there we go, but if it is the goal but nto the start, 
    # we go through all of come-from and append it to our path. 
    # If we still haven't found our goal, we search neighbors and calculte the f_score and iterate using that
    while open_list: 
        f_score, current = heapq.heappop(open_list) #takes the lowest f_score and makes it the current
        if current == goal:
            path = []
            while current != start: 
                path.append(current)
                current = come_from[current]
            return path
        if current != goal:
            neighbors = get_neighbors(current, grid)
            for neighbor in neighbors:
                new_g = g_score[current] + 1 #how far did we already go
                h_score = heuristic(neighbor, goal) #how far do we have to go
                f_score = new_g + h_score # cost of actually going there
                if neighbor not in g_score or new_g < g_score[neighbor]: #did we see this before or if we have is it worth exploring for cost
                    g_score[neighbor] = new_g
                    come_from[neighbor] = current
                    heapq.heappush(open_list, (f_score, neighbor))
    return None

if __name__ == "__main__":
    path = astar(grid, goal, start)
    print(path)




print(get_neighbors(start, grid))
print(heuristic(start, goal))
