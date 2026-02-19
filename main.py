import pygame

pygame.init()

WINDOW_HEIGHT = int(input("What would you like the height to be: "))
WINDOW_WIDTH = int(input("What would you like the width to be: "))
cell_dimension = int(input("What size do you want the cells to be: "))
white_colour = (200, 200, 200)
start_colour = (0, 255, 0)
destination = (255, 0, 0)

start_cell = None
goal_cell = None
painting = False
obstacle_cells = set()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Our window")


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, cell_dimension):
        pygame.draw.line(surface, white_colour, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, cell_dimension):
        pygame.draw.line(surface, white_colour, (0, y), (WINDOW_WIDTH, y))


def clicked_cell(cell_posn):
    cell_x, cell_y = cell_posn
    col = cell_x // cell_dimension
    row = cell_y // cell_dimension
    return row, col


def fill_cell(surface, x, y, color):
    x = col * cell_dimension
    y = row * cell_dimension
    rect = pygame.rect(y, x, cell_dimension, cell_dimension)
    pygame.draw.rect(surface, color, rect)


def add_obstacle(cell):
    if cell != start_cell and cell != goal_cell:
        obstacle_cells.add(cell)


program_run = True

while program_run:
    window.fill((0, 0, 0))
    pygame.time.delay(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = clicked_cell(event.pos)
            cell = (row, col)
            # print(event)

            if event.button == 2:
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
            elif event.button == 3:
                if cell != start_cell not in obstacle_cells:
                    goal_cell = cell
                    print(f"The goal cell is {cell}")

    draw_grid(window)
    pygame.display.flip()


pygame.quit()
