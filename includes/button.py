"""Button

A module for button in pygame
"""
import re
from typing import Any, Callable, Literal
from threading import Thread
import pygame

NORMAL = "normal"
DISABLED = "disabled"
WHITE = "#FFFFFF"
DEF_DISABLED_STATE = "#9c9c9c"
DEF_NORMAL_STATE = "#475F77"
DEF_DOWN_STATE = "#D74B4B"
HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"

class Button:
    """Button

    Pygame widget Button
    """
    def __init__(self, master: pygame.Surface, font: pygame.font.Font, text: str | None = ...,
                 command: Callable[[], Any] | str = ...,
                 state: Literal["normal", "disabled"] = "normal", border_radius: int | None = 0,
                 text_bg_color: str = WHITE, disabled_color: str = DEF_DISABLED_STATE,
                 normal_color: str = DEF_NORMAL_STATE, click_color: str = DEF_DOWN_STATE):
        """Button:

        Args:
            master (pygame.Surface): A surface to draw on
            font (pygame.font.Font): Pygame font, for rendering text.
            text (str | None, optional): Text to render on Button. Optional.
            command (Callable[[], Any] | str, optional):
                Function to be called when button is pressed. Optional
            state (Literal["normal", "disabled"], optional):
                Default state for button. Defaults to "normal"
            border_radius (int | None, optional):
                Increase this number make button edges rounder. Defaults to -1
        """
        if isinstance(master, pygame.Surface):
            self.screen = master
        elif not isinstance(master, pygame.Surface):
            raise TypeError(f"invalid type for master: {type(master)}. Expected: pygame.Surface")
        if isinstance(font, pygame.font.Font):
            self.font = font
        elif not isinstance(font, pygame.font.Font):
            raise TypeError(f"invalid type for font: {type(font)}. Expected: pygame.font.Font")
        if isinstance(text, str):
            self.text = text
        else:
            raise TypeError(f"invalid type for text: {type(text)}. Expected: str")
        if command and callable(command):
            self.command = command
        else:
            self.command = lambda: None
        if isinstance(state, str):
            self.state = state.lower()
            if self.state not in ("normal", "disabled"):
                raise ValueError(f"invalid value for state: {state}. Expected: \"normal\""
                                 "or \"disabled\"")
        else:
            raise TypeError(f"invalid type for state: {type(state)}. Expected: str")
        if isinstance(border_radius, int):
            self.border_radius = border_radius
        else:
            raise TypeError(f"invalid type for border_radius: {type(border_radius)}."
                            " Expected: str")
        if isinstance(text_bg_color, str):
            if re.match(HEX_COLOR_PATTERN, text_bg_color):
                self.text_bg_color = text_bg_color
            else:
                raise ValueError(f"invalid value for text_bg_color: {text_bg_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for text_bg_color: {type(text_bg_color)}."
                            " Expected: str")
        if isinstance(disabled_color, str):
            if re.match(HEX_COLOR_PATTERN, disabled_color):
                self.disabled_color = disabled_color
            else:
                raise ValueError(f"invalid value for disabled_color: {disabled_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for disabled_color: {type(disabled_color)}."
                            " Expected: str")
        if isinstance(normal_color, str):
            if re.match(HEX_COLOR_PATTERN, normal_color):
                self.normal_color = normal_color
            else:
                raise ValueError(f"invalid value for normal_color: {normal_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for normal_color: {type(normal_color)}."
                            " Expected: str")
        if isinstance(click_color, str):
            if re.match(HEX_COLOR_PATTERN, click_color):
                self.click_color = click_color
            else:
                raise ValueError(f"invalid value for click_color: {click_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for click_color: {type(click_color)}."
                            " Expected: str")
        if self.state == NORMAL:
            self.button_color = self.normal_color
        else:
            self.button_color = self.disabled_color
        self.pressed = False
        self.function_executed = False


    def place(self, x: int, y: int, width: int, height: int):
        """Place button on Surface

        Args:
            x (int): Position on x-axis
            y (int): Position on y-axis
            width (int): Button's width
            height (int): Button's height
        """
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.text_surface = self.font.render(self.text, True, self.text_bg_color)
        self.text_rect = self.text_surface.get_rect(
            center=self.top_rect.center)
        self.text_rect.center = self.top_rect.center

        pygame.draw.rect(self.screen, self.button_color, self.top_rect,
                         border_radius=self.border_radius)
        self.screen.blit(self.text_surface, self.text_rect)
        self.check_click()


    def config(self, text: str | None = ..., font: pygame.font.Font | None = ...,
               command: Callable[[], Any] | str = ..., border_radius: int | None = ...,
               state: Literal["normal", "disabled"] = ...,
               text_bg_color: str = ..., disabled_color: str = ...,
               normal_color: str = ..., click_color: str = ...):
        """Configure button attributes

        Args:
            text (str | None, optional): Change button text. Optional
            font (pygame.font.Font | None, optional): Change button font. Optional
            command (Callable[[], Any] | str, optional): Change command called. Optional
            border_radius (int | None, optional): Change border radius. Optional
            state (Literal["normal", "disabled"]): Change button state. Optional

        Raises:
            PassingWrongValue: Passing wrong value to state
        """
        if isinstance(text, str):
            self.text = text
        if isinstance(font, pygame.font.Font):
            self.font = font
        if callable(command):
            self.command = command
        if isinstance(state, str):
            if state not in ("disabled", "normal"):
                raise ValueError(f"invalid value for state: {state}. Expected: "
                                 "\"normal\" or \"disabled\"")
            self.state = state.lower()
            if self.state == NORMAL:
                self.button_color = self.normal_color
            elif self.state == DISABLED:
                self.button_color = self.disabled_color
        if isinstance(border_radius, int) and border_radius >= 0:
            self.border_radius = border_radius
        if isinstance(text_bg_color, str) and re.match(HEX_COLOR_PATTERN, text_bg_color):
            self.text_bg_color = text_bg_color
        if isinstance(disabled_color, str) and re.match(HEX_COLOR_PATTERN, disabled_color):
            self.disabled_color = disabled_color
        if isinstance(normal_color, str) and re.match(HEX_COLOR_PATTERN, normal_color):
            self.normal_color = normal_color
        if isinstance(click_color, str) and re.match(HEX_COLOR_PATTERN, click_color):
            self.click_color = click_color


    def check_click(self):
        """Check button click
        """
        if self.state == DISABLED:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.top_rect.collidepoint(mouse_pos):
            return
        if pygame.mouse.get_pressed()[0]:
            self.button_color = self.click_color
            self.pressed = True
        wc = lambda: Thread(target=self.wait_click).start()
        wc()


    def wait_click(self):
        if not self.pressed:
            return
        while pygame.mouse.get_pressed()[0]:
            continue
        if not pygame.mouse.get_pressed()[0] and not self.function_executed:
            Thread(target=self.command).start()
            self.function_executed = True
        self.pressed = False
        self.function_executed = False
        self.button_color = self.normal_color
