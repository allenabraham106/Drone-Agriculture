import pygame

class Drone: 
    def __init__(self, path, cell_dimension, yeild_zones):
        self.path = path
        self.index = 0
        self.timer = 0
        self.active = False
        self.image = pygame.image.load("drone.png")
        self.image = pygame.transform.scale(self.image, (cell_dimension * 3, cell_dimension * 3))   
        self.yeild_zones = yeild_zones
        self.yeild_score = 0
        self.yeild_values = {
            "high": 3,
            "medium": 2,
            "low": 1
        }
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
                else: 
                    cell = self.path[self.index]
                    zone = self.yeild_zones.get(cell, "low")
                    self.yeild_score += self.yeild_values[zone]
    def draw(self, surface, cell_dimension):
        if self.active and self.index < len(self.path):
            row, col = self.path[self.index]
            y = row * cell_dimension
            x = col * cell_dimension
            surface.blit(self.image, (x - cell_dimension, y - cell_dimension))