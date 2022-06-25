import math
from typing import Any

import pygame

from light.includes.constants import BLACK, WIDTH, HEIGHT, CENTER, RED, \
    AIR, GLASS

class IncidentRay:
    def __init__(self, master: pygame.Surface, angle: Any, font: pygame.font.Font):
        self.__screen = master
        self.__x = WIDTH / 2
        self.__y = 0
        self.__ray_length = 400
        self.__angle_f = 0
        self.__angle = angle
        self.__font = font
            
    def config(self, angle):
        self.__angle = angle
        
    def update(self):
        if 0 < self.__angle:
            self.__x = 0
            self.__y = HEIGHT / 2
        if -180 <= self.__angle <= -90:
            self.__x = CENTER[0] + math.cos(math.radians(self.__angle)) * self.__ray_length
            self.__y = CENTER[1] + math.sin(math.radians(self.__angle)) * self.__ray_length
            self.__angle_f = 180 - self.__angle - 270 + 270
            text_surface = self.__font.render(f"I : {(180 - self.__angle - 270)}", False, BLACK)
            self.__screen.blit(text_surface, (20, 470))

    @property
    def angle_f(self):
        return self.__angle_f
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    @angle_f.setter
    def angle_f(self, value):
        self.__angle_f = value
    @x.setter
    def x(self, value):
        self.__x = value
    @y.setter
    def y(self, value):
        self.__y = value

    def display(self):
        self.update()
        pygame.draw.line(self.__screen, RED, CENTER, (self.__x, self.__y), 3)

class ReflectedRay:
    def __init__(self, screen: pygame.Surface, angle: int):
        self.__screen = screen
        self.__ray_length = 400
        self.__angle = angle
        self.__x = WIDTH / 2
        self.__y = 0

    def config(self, angle):
        self.__angle = angle
        
    def update(self):
        self.__reflected_angle = 180 - self.__angle
        if 270 <= self.__reflected_angle <= 360:
            self.__x = CENTER[0] + math.cos(math.radians(self.__reflected_angle)) * self.__ray_length
            self.__y = CENTER[1] + math.sin(
                math.radians(self.__reflected_angle)
            ) * self.__ray_length
        if 180 > self.__reflected_angle >= 0:
            self.__x = WIDTH
            self.__y = HEIGHT / 2

    def display(self):
        self.update()
        pygame.draw.line(self.__screen, RED, CENTER, (self.__x, self.__y), 3)


class RefractedRay:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, angle: int):
        self.__screen = screen
        self.__x = WIDTH / 2
        self.__y = 0
        self.__angle = angle
        self.__ray_length = 400
        self.__font = font
        
        self.__air_material = AIR
        self.__surface_material = GLASS

    def config_material(self, air_material, surface_material):
        self.__air_material = air_material
        self.__surface_material = surface_material
        
    def config(self, angle):
        self.__angle = angle
        
    def update(self):
        self.__true_angle = (180 - self.__angle - 270)
        self.__refracted_angle = -math.degrees(
            math.asin(math.sin(math.radians(self.__true_angle)) *
                      self.__air_material[0] / self.__surface_material[0])
        ) + 90
        if 0 < self.__angle:
            self.__x = 0
            self.__y = HEIGHT / 2
        if -180 <= self.__angle <= -90:
            self.__x = CENTER[0] + math.cos(
                math.radians(self.__refracted_angle)) * self.__ray_length
            self.__y = CENTER[1] + math.sin(
                math.radians(self.__refracted_angle)) * self.__ray_length
            text_surface1 = self.__font.render(f"R  : {((self.__refracted_angle - 90) * -1)}",
                                               False, (0, 0, 0))
            text_surface2 = self.__font.render(f"N1 : {self.__air_material[0]}",
                                               False, (0, 0, 0))
            text_surface3 = self.__font.render(f"N2 : {self.__surface_material[0]}",
                                               False, (0, 0, 0))
            self.__screen.blit(text_surface1, (20, 500))
            self.__screen.blit(text_surface2, (20, 150))
            self.__screen.blit(text_surface3, (20, 400))

    def display(self):
        self.update()
        pygame.draw.line(self.__screen, RED, CENTER, (self.__x, self.__y), 3)


class RefractionSurface:
    def __init__(self, screen: pygame.Surface):
        self.__screen = screen
        self.surface = pygame.Surface((WIDTH, HEIGHT/2), pygame.SRCALPHA)
        self.surface.fill("#0C38E864")
        
    def display(self):
        self.__screen.blit(self.surface, (0, HEIGHT / 2))