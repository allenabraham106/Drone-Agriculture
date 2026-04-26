import pygame

class Drone: 
    def __init__(self, path, cell_dimension):
        self.path = path
        self.index = 0
        self.timer = 0
        self.active = False
        self.image = pygame.image.load("drone.png")
        self.image = pygame.transform.scale(self.image, (cell_dimension * 3, cell_dimension * 3))   
    def start(self):
        self.active = True
    def update(self):
        if self.active: 
            self.timer += 1
            if self.timer >= 10:
                self.timer = 0
                self.index += 1
                if self.index >= len(self.path):
                    self.active = False
    def draw(self, surface, cell_dimension):
        if self.active and self.index < len(self.path):
            row, col = self.path[self.index]
            y = row * cell_dimension
            x = col * cell_dimension
            surface.blit(self.image, (x - cell_dimension, y - cell_dimension))