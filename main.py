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
        pygame.draw.line(surface, white_colour, (0, y), (GRID_WIDTH, y))


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

def draw_panel(surface, path_length, current_zone, yield_score, efficiency):
    pygame.draw.rect(surface, (30, 30, 30), (GRID_WIDTH, 0, 200, WINDOW_HEIGHT))
    font = pygame.font.SysFont("Ariel", 16)
    title = font.render("Ag-Drone", True, (255,255,255))
    surface.blit(title, (GRID_WIDTH + 10, 20))

    pygame.draw.rect(surface, (0, 200, 0), (GRID_WIDTH + 10, 80, 15, 15))
    surface.blit(font.render("High Yield", True, (255, 255, 255)), (GRID_WIDTH + 30, 80))

    pygame.draw.rect(surface, (255, 165, 0), (GRID_WIDTH + 10, 100, 15, 15))
    surface.blit(font.render("Medium Yield", True, (255, 255, 255)), (GRID_WIDTH + 30, 100))

    pygame.draw.rect(surface, (255, 255, 0), (GRID_WIDTH + 10, 120, 15, 15))
    surface.blit(font.render("Low Yield", True, (255, 255, 255)), (GRID_WIDTH + 30, 120))

    surface.blit(font.render(f"Path length: {path_length}", True, (255, 255, 255)), (GRID_WIDTH + 10, 160))
    surface.blit(font.render(f"Zone: {current_zone}", True, (255, 255, 255)), (GRID_WIDTH + 10, 200))

    surface.blit(
        font.render("Controls:", True, (200, 200, 200)), (GRID_WIDTH + 10, 280)
    )
    surface.blit(
        font.render("L-Click: Set Start", True, (200, 200, 200)), (GRID_WIDTH + 10, 300)
    )
    surface.blit(font.render("G: Set Goal", True, (200, 200, 200)), (GRID_WIDTH + 10, 320))
    surface.blit(
        font.render("R-Click: Obstacle", True, (200, 200, 200)), (GRID_WIDTH + 10, 340)
    )
    surface.blit(
        font.render("Space: Run Drone", True, (200, 200, 200)), (GRID_WIDTH + 10, 360)
    )
    surface.blit(font.render("R: New Farm", True, (200, 200, 200)), (GRID_WIDTH + 10, 380))

    surface.blit(
        font.render(f"Yield Score: {yield_score}", True, (255, 255, 255)),
        (GRID_WIDTH + 10, 220),
    )

    surface.blit(
        font.render(f"Yield %: {efficiency:.1f}%", True, (255, 255, 255)),
        (GRID_WIDTH + 10, 240),
    )


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
        score = drone.yeild_score
    else:
        score = 0
    
    
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
                    cols = GRID_WIDTH // cell_dimension
                    grid = [[0 for _ in range(cols)] for _ in range(rows)] #building the grid
                    for obstacles in obstacle_cells:
                        grid[obstacles[0]][obstacles[1]] = 1
                    current_path = astar(grid, goal_cell, start_cell, yeild_zones)
                    drone = Drone(current_path, cell_dimension, yeild_zones)
                    drone.start()
                    print(current_path)
            elif event.key == pygame.K_r:
                yeild_zones = generate_farm(rows, cols)
                current_path = []
                start_cell = None
                goal_cell = None
    
    if drone and len(current_path) > 0:
        max_score = len(current_path) * 3 # for the high-yeild value
        efficieny = (drone.yeild_score/max_score) * 100
    else: 
        max_score = 0
        efficieny = 0
    if drone and drone.index < len(current_path):
        current_zone = yeild_zones.get(current_path[drone.index], "-")
    else:
        current_zone = "-"
    
    
    draw_grid(window)
    draw_panel(window, len(current_path), current_zone, score, efficieny)
    pygame.display.flip()


pygame.quit()
