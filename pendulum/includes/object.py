import re
import math
import pygame


HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"
DEF_LINE_COLOR = "#000000"
DEF_BORDER_COLOR = "#000000"
DEF_FILL_COLOR = "#960000"

class Pendulum:
    def __init__(self, coords: list | tuple = ..., radius: int = ..., balance: int = ...):
        self.x = coords[0]
        self.y = coords[1]
        self.old_x = coords[0]
        self.old_y = coords[1]
        self.radius = radius
        self.balance = balance
        self.vel = 0
        self.angacc = 0

    def angle_length(self):
        self.length = math.sqrt(math.pow(self.x - self.balance, 2)
                            + math.pow(self.y - 50, 2))
        self.angle = math.asin((self.x - self.balance) / self.length)

    def update_position(self):
        self.x = round(self.balance + self.length * math.sin(self.angle))
        self.y = round(50 + self.length * math.cos(self.angle))

    def draw(self, screen: pygame.Surface, click_region: pygame.Surface,
             line_color: str = DEF_LINE_COLOR, border_color: str = DEF_BORDER_COLOR,
             fill_color: str = DEF_FILL_COLOR):
        if not isinstance(screen, pygame.Surface):
            raise TypeError("screen must be a pygame.Surface")
        if not isinstance(click_region, pygame.Surface):
            raise TypeError("click_region must be a pygame.Surface")
        if not re.match(HEX_COLOR_PATTERN, line_color) or not isinstance(line_color, str):
            line_color = DEF_LINE_COLOR
        if not re.match(HEX_COLOR_PATTERN, border_color) or not isinstance(border_color, str):
            border_color = DEF_BORDER_COLOR
        if not re.match(HEX_COLOR_PATTERN, fill_color) or not isinstance(fill_color, str):
            fill_color = DEF_FILL_COLOR
        pygame.draw.lines(screen, line_color, False,
                          [(self.balance, 50), (self.x, self.y)], 2)
        pygame.draw.circle(screen, border_color,
                           (self.x, self.y), self.radius)
        pygame.draw.line(click_region, fill_color,
                         (self.old_x, self.old_y),
                         (self.x, self.y), 2)
        screen.blit(click_region, (0, 0))
        pygame.draw.circle(screen, fill_color,
                           (self.x, self.y), self.radius - 2)