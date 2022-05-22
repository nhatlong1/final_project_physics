"""Label

A module for Label in pygame
"""

from typing import Literal
import re
import pygame

BLACK = "#000000"
LIGHT_GRAY2 = "#EcEcEc"
HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"

class Label:
    """Label
    Label widget for pygame

    Args:
        master (pygame.Surface): Surface to draw on
        font (pygame.font.Font): Pygame font for rendering text
        text (str | None, optional): Display text
        _fg (str | None, optional): foreground color (text color)
        _bg (str | None, optional): background color
        border_radius (int | None, optional): border roundness
        justify: Text position inside textbox. Currently allow
            "center", "left", "right"
    """
    def __init__(self, master: pygame.Surface, font: pygame.font.Font, text: str | None = ...,
                 fg: str | None = ..., bg: str | None = ..., border_radius: int | None = ...,
                 justify: Literal["left", "right", "center"] = ...):
        self.pattern = HEX_COLOR_PATTERN
        if master and isinstance(master, pygame.Surface):
            self.screen = master
        elif not isinstance(master, pygame.Surface):
            raise TypeError("master must be a Surface")
        if font and isinstance(font, pygame.font.Font):
            self.font = font
        elif not isinstance(font, pygame.font.Font):
            raise TypeError("font must be pygame.font.Font")
        if fg and isinstance(fg, str):
            if re.match(self.pattern, fg):
                self._fg = fg
            else:
                self._fg = BLACK
        else:
            self._fg = BLACK
        if bg and isinstance(bg, str):
            if re.match(self.pattern, bg):
                self._bg = bg
            else:
                self._bg = LIGHT_GRAY2
        else:
            self._bg = LIGHT_GRAY2
        if border_radius and isinstance(border_radius, int):
            self.border_radius = border_radius
        else:
            self.border_radius = -1
        if justify and justify in ("left", "right", "center"):
            self.justify = justify
        else:
            self.justify = "center"
        self.text = text


    def place(self, x: int, y: int,
              width: int | None = ..., height: int | None = ...):
        """Place widget on screen

        Args:
            x (int): Posituion on x-axis
            y (int): Position on y-axis
            width (int | None, optional): Label width.
            height (int | None, optional): Label height.
        Omitting width or height will automatically set them to match text
        width and height
        """
        use_justify = True
        if not isinstance(x, int):
            raise ValueError("x must be int")
        if not isinstance(y, int):
            raise ValueError("y must be int")

        if not width or (not isinstance(width, int) and not isinstance(width, float)):
            width = self.font.size(self.text)[0]
            use_justify = False
        if not height or (not isinstance(height, int) and not isinstance(height, float)):
            height = self.font.size(self.text)[1]

        self.top_rect = pygame.Rect((x, y, width, height))
        self.text_surface = self.font.render(self.text, True, self._fg)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centery = self.top_rect.centery
        if use_justify:
            match self.justify:
                case "left":
                    self.text_rect.left = self.top_rect.left
                case "right":
                    self.text_rect.right = self.top_rect.right
                case "center":
                    self.text_rect.center = self.top_rect.center
                case _:
                    pass

        pygame.draw.rect(self.screen, self._bg, self.top_rect,
                         border_radius=self.border_radius)
        self.screen.blit(self.text_surface, self.text_rect)

    def config(self, text: str | None = ..., font: pygame.font.Font | None = ...,
               fg: str | None = ..., bg: str | None = ..., border_radius: int | None = ...,
               justify: Literal["left", "right", "center"] = ...):
        """Configure Label widget

        Args:
            text (str | None, optional): Change text
            font (pygame.font.Font | None, optional): Change font
            fg (str | None, optional): Change text color
            bg (str | None, optional): Change label background color
            border_radius (int | None, optional): Change border roundness
            justify: Change justify
        """
        if text and isinstance(text, str):
            self.text = text
        if font and isinstance(font, pygame.font.Font):
            self.font = font
        if fg and isinstance(fg, str) and re.match(self.pattern, fg):
            self._fg = fg
        if bg and isinstance(bg, str) and re.match(self.pattern, bg):
            self._bg = bg
        if border_radius and isinstance(border_radius, int):
            self.border_radius = border_radius
        if justify and justify in ("left", "right", "center"):
            self.justify = justify
