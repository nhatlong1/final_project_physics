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
                 command: Callable[[], Any] | str = ..., args: list | tuple = (),
                 use_thread: bool = True,
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
            args (list, tuple, optional): A list/tuple of arguments to pass in command
            state (Literal["normal", "disabled"], optional):
                Default state for button. Defaults to "normal"
            border_radius (int | None, optional):
                Increase this number make button edges rounder. Defaults to -1
        """
        if isinstance(master, pygame.Surface):
            self.__screen = master
        elif not isinstance(master, pygame.Surface):
            raise TypeError(f"invalid type for master: {type(master)}. Expected: pygame.Surface")
        if isinstance(font, pygame.font.Font):
            self.__font = font
        elif not isinstance(font, pygame.font.Font):
            raise TypeError(f"invalid type for font: {type(font)}. Expected: pygame.font.Font")
        if isinstance(text, str):
            self.__text = text
        else:
            raise TypeError(f"invalid type for text: {type(text)}. Expected: str")
        if command and callable(command):
            self.__command = command
        else:
            self.__command = lambda: None
        if isinstance(args, list | tuple):
            self.__args = args
        else:
            raise TypeError(f"invalid type for args: {type(args)}. Expected: list, tuple")
        if isinstance(use_thread, bool):
            self.__use_thread = use_thread
        else:
            raise TypeError(f"invalid type for use_thread: {type(use_thread)}. Expected: bool")
        if isinstance(state, str):
            self.__state = state.lower()
            if self.__state not in ("normal", "disabled"):
                raise ValueError(f"invalid value for state: {state}. Expected: \"normal\""
                                 "or \"disabled\"")
        else:
            raise TypeError(f"invalid type for state: {type(state)}. Expected: str")
        if isinstance(border_radius, int):
            self.__border_radius = border_radius
        else:
            raise TypeError(f"invalid type for border_radius: {type(border_radius)}."
                            " Expected: str")
        if isinstance(text_bg_color, str):
            if re.match(HEX_COLOR_PATTERN, text_bg_color):
                self.__text_color = text_bg_color
            else:
                raise ValueError(f"invalid value for text_bg_color: {text_bg_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for text_bg_color: {type(text_bg_color)}."
                            " Expected: str")
        if isinstance(disabled_color, str):
            if re.match(HEX_COLOR_PATTERN, disabled_color):
                self.__disabled_color = disabled_color
            else:
                raise ValueError(f"invalid value for disabled_color: {disabled_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for disabled_color: {type(disabled_color)}."
                            " Expected: str")
        if isinstance(normal_color, str):
            if re.match(HEX_COLOR_PATTERN, normal_color):
                self.__normal_color = normal_color
            else:
                raise ValueError(f"invalid value for normal_color: {normal_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for normal_color: {type(normal_color)}."
                            " Expected: str")
        if isinstance(click_color, str):
            if re.match(HEX_COLOR_PATTERN, click_color):
                self.__click_color = click_color
            else:
                raise ValueError(f"invalid value for click_color: {click_color}."
                                 " Please use a valid 6-digit HEX number")
        else:
            raise TypeError(f"invalid type for click_color: {type(click_color)}."
                            " Expected: str")
        if self.__state == NORMAL:
            self.__button_color = self.__normal_color
        else:
            self.__button_color = self.__disabled_color
        self.__pressed = False
        self.__function_executed = False


    def place(self, x: int, y: int, width: int, height: int):
        """Place button on Surface

        Args:
            x (int): Position on x-axis
            y (int): Position on y-axis
            width (int): Button's width
            height (int): Button's height
        """
        self.__top_rect = pygame.Rect((x, y), (width, height))
        self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
        self.__text_rect = self.__text_surface.get_rect(
            center=self.__top_rect.center)
        self.__text_rect.center = self.__top_rect.center

        pygame.draw.rect(self.__screen, self.__button_color, self.__top_rect,
                         border_radius=self.__border_radius)
        self.__screen.blit(self.__text_surface, self.__text_rect)
        self.check_click()


    def config(self, text: str | None = ..., font: pygame.font.Font | None = ...,
               command: Callable[[], Any] | str = ..., border_radius: int | None = ...,
               state: Literal["normal", "disabled"] = ..., args: list | tuple | None = ...,
               text_color: str = ..., disabled_color: str = ...,
               normal_color: str = ..., click_color: str = ...):
        """Configure button attributes

        Args:
            text (str | None, optional): Change button text. Optional
            font (pygame.font.Font | None, optional): Change button font. Optional
            command (Callable[[], Any] | str, optional): Change command called. Optional
            border_radius (int | None, optional): Change border radius. Optional
            state (str): Enable/disable button
            text_color (str): text color
            disabled_color (str): Color when button is disabled
            normal_color (str): Color when button is idle
            click_color (str): Color when button is clicked

        Raises:
            PassingWrongValue: Passing wrong value to state
        """
        if isinstance(text, str):
            self.__text = text
        if isinstance(font, pygame.font.Font):
            self.__font = font
        if callable(command):
            self.__command = command
        if isinstance(state, str):
            if state not in ("disabled", "normal"):
                raise ValueError(f"invalid value for state: {state}. Expected: "
                                 "\"normal\" or \"disabled\"")
            self.__state = state.lower()
            if self.__state == NORMAL:
                self.__button_color = self.__normal_color
            elif self.__state == DISABLED:
                self.__button_color = self.__disabled_color
        if isinstance(args, tuple | list):
            self.__args = tuple(args)
        if isinstance(border_radius, int) and border_radius >= 0:
            self.__border_radius = border_radius
        if isinstance(text_color, str) and re.match(HEX_COLOR_PATTERN, text_color):
            self.__text_color = text_color
        if isinstance(disabled_color, str) and re.match(HEX_COLOR_PATTERN, disabled_color):
            self.__disabled_color = disabled_color
        if isinstance(normal_color, str) and re.match(HEX_COLOR_PATTERN, normal_color):
            self.__normal_color = normal_color
        if isinstance(click_color, str) and re.match(HEX_COLOR_PATTERN, click_color):
            self.__click_color = click_color


    def check_click(self):
        """Check button click
        """
        if self.__state == DISABLED:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.__top_rect.collidepoint(mouse_pos):
            return
        if pygame.mouse.get_pressed()[0]:
            self.__button_color = self.__click_color
            self.__pressed = True
            wc = lambda: Thread(target=self.wait_click).start()
            wc()
        else:
            wc = Thread(target=self.wait_click)
            wc.start()
            wc.join()


    def wait_click(self):
        if not self.__pressed:
            return
        while pygame.mouse.get_pressed()[0]:
            continue
        if not pygame.mouse.get_pressed()[0] and not self.__function_executed:
            if self.__use_thread and self.__args:
                self.__function_executed = True
                cd = Thread(target=self.__command, args=tuple(self.__args))
                cd.start()
                self.__function_executed = False
            elif self.__use_thread and not self.__args:
                self.__function_executed = True
                cd = Thread(target=self.__command)
                cd.start()
                self.__function_executed = False
            elif not self.__use_thread and self.__args:
                self.__function_executed = True
                self.__command(*self.__args)
                self.__function_executed = False
            elif not self.__use_thread and not self.__args:
                self.__function_executed = True
                self.__command()
                self.__function_executed = False
        self.__pressed = False
        self.__button_color = self.__normal_color
