from astar import astar
from farm import generate_farm, yield_colours
from drone import Drone
import pygame

pygame.init()

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
GRID_WIDTH = 800
cell_dimension = 20
white_colour = (200, 200, 200)
start_colour = (0, 255, 0)
destination = (255, 0, 0)
obstacle_color = (128, 128, 128)
pathway = (0,0 ,255)
start_cell = None
goal_cell = None
painting = False
obstacle_cells = set()
current_path = []
drone_image = pygame.image.load("Drone.png")
drone_image = pygame.transform.scale(drone_image, (cell_dimension, cell_dimension))
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Our window")
rows = WINDOW_HEIGHT // cell_dimension
cols = WINDOW_WIDTH // cell_dimension
yeild_zones = generate_farm(rows, cols)
drone = None


def draw_grid(surface):
    for x in range(0, GRID_WIDTH, cell_dimension):
        pygame.draw.line(surface, white_colour, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, cell_dimension):
        pygame.draw.line(surface, white_colour, (0, y), (WINDOW_WIDTH, y))


def clicked_cell(cell_posn):
    cell_x, cell_y = cell_posn
    col = cell_x // cell_dimension
    row = cell_y // cell_dimension
    return row, col


def fill_cell(surface, row, col, color):
    x = col * cell_dimension
    y = row * cell_dimension
    rect = pygame.Rect(x, y, cell_dimension, cell_dimension)
    pygame.draw.rect(surface, color, rect)


def add_obstacle(cell):
    if cell != start_cell and cell != goal_cell:
        obstacle_cells.add(cell)

def draw_panel(surface):
    

program_run = True

while program_run:
    window.fill((0, 0, 0))
    pygame.time.delay(60)

    for (row, col), level in yeild_zones.items():
        fill_cell(window, row, col, yield_colours[level])

    if start_cell: 
        row,col = start_cell
        fill_cell(window, row, col, start_colour)

    if goal_cell:
        row,col = goal_cell
        fill_cell(window, row, col, destination)

    for cell in obstacle_cells:
        row,col = cell
        fill_cell(window, row, col, obstacle_color)

    if current_path and drone:
        for cell in current_path[:drone.index]:
            row, col = cell
            fill_cell(window, row, col, pathway)
    
    if drone:
        drone.update()
        drone.draw(window, cell_dimension)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = clicked_cell(event.pos)
            cell = (row, col)
            # print(event)
            if event.button == 3:
                if (row, col) in obstacle_cells:
                    obstacle_cells.remove((row, col))
                else:
                    if cell != start_cell and cell != goal_cell:
                        obstacle_cells.add((row, col))
                        print(f"Obstacle at {cell}")
            elif event.button == 1:
                if cell not in obstacle_cells:
                    start_cell = cell
                    print(f"The start Cell is {cell}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                if goal_cell == None:
                    goal_cell = clicked_cell(pygame.mouse.get_pos())
            elif event.key == pygame.K_SPACE:
                if goal_cell and start_cell: 
                    rows = WINDOW_HEIGHT // cell_dimension
                    cols = WINDOW_WIDTH // cell_dimension
                    grid = [[0 for _ in range(cols)] for _ in range(rows)] #building the grid
                    for obstacles in obstacle_cells:
                        grid[obstacles[0]][obstacles[1]] = 1
                    current_path = astar(grid, goal_cell, start_cell, yeild_zones)
                    drone = Drone(current_path, cell_dimension)
                    drone.start()
                    print(current_path)
            elif event.key == pygame.K_r:
                yeild_zones = generate_farm(rows, cols)
                current_path = []
                start_cell = None
                goal_cell = None
    draw_grid(window)
    pygame.display.flip()


pygame.quit()
