"""Button

A module for button in pygame
"""
from pathlib import PosixPath, WindowsPath, Path
import re
from typing import Any, Callable, Literal
from threading import Thread
import pygame

_NORMAL = "normal"
_DISABLED = "disabled"
_WHITE = "#FFFFFF"
_DEF_DISABLED_STATE = "#9c9c9c"
_DEF_NORMAL_STATE = "#475F77"
_DEF_DOWN_STATE = "#D74B4B"
_HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"
_TYPE_MSG = lambda name, param, expect: f"invalid type for {name}: {param}. Expected: {expect}"
_VAL_MSG = lambda name, param, expect: f"invalid value for {name}: {param}. Expected: {expect}"

class Button:
    """Button

    Pygame widget Button
    """
    def __init__(self, master: pygame.Surface,
                 font: pygame.font.Font,
                 text: str | None = ...,
                 command: Callable[[], Any] | str = ...,
                 args: list | tuple = (),
                 image: str | pygame.Surface | PosixPath | WindowsPath | None = None,
                 use_thread: bool = True,
                 allow_hold: bool = False,
                 state: Literal["normal", "disabled"] = "normal",
                 border_radius: int | None = 0,
                 text_color: str = _WHITE,
                 disabled_color: str = _DEF_DISABLED_STATE,
                 normal_color: str = _DEF_NORMAL_STATE,
                 click_color: str = _DEF_DOWN_STATE):
        """Button:

        Args:
            master (pygame.Surface): A surface to draw on
            font (pygame.font.Font): Pygame font, for rendering text.
            text (str | None, optional): Text to render on Button. Optional.
            image (str | pygame.Surface | PosixPath | WindowsPath | None, optional): Image
            for button
            command (Callable[[], Any] | str, optional):
                Function to be called when button is pressed. Optional
            args (list, tuple, optional): A list/tuple of arguments to pass in command
            use_thread (bool, optional): Use thread to run command.
            allow_hold (bool, optional): Allow user to hold button. WIP
            state (Literal["normal", "disabled"], optional):
                Default state for button. Defaults to "normal"
            border_radius (int | None, optional):
                Increase this number make button edges rounder. Defaults to -1
            text_color (str, optional): Text color
            disabled_color (str, optional): Disabled button color
            normal_color (str, optional): Idle color
            click_color (str, optional): Color when button is clicked
        """
        if isinstance(master, pygame.Surface):
            self.__screen = master
        elif not isinstance(master, pygame.Surface):
            raise TypeError(_TYPE_MSG("master", master, "pygame.Surface"))
        if isinstance(font, pygame.font.Font):
            self.__font = font
        elif not isinstance(font, pygame.font.Font):
            raise TypeError(_TYPE_MSG("font", type(font), "pygame.font.Font"))
        if isinstance(text, str):
            self.__text = text
        else:
            raise TypeError(_TYPE_MSG(type(text), "str"))
        if not isinstance(image, str | pygame.Surface | PosixPath | WindowsPath | None):
            raise TypeError(_TYPE_MSG("image", type(image), "str, pygame.Surface, Path, None"))
        if command and callable(command):
            self.__command = command
        else:
            self.__command = lambda: None
        if isinstance(args, list | tuple):
            self.__args = args
        else:
            raise TypeError(_TYPE_MSG("args", type(args), "list, tuple"))
        if isinstance(use_thread, bool):
            self.__use_thread = use_thread
        else:
            raise TypeError(_TYPE_MSG("use_thread", type(use_thread), "bool"))
        if isinstance(state, str):
            self.__state = state.lower()
            if self.__state not in ("normal", "disabled"):
                raise ValueError(_VAL_MSG("state", state, "\"normal\", \"disabled\""))
        else:
            raise TypeError(_TYPE_MSG("state", state, "str"))
        if isinstance(border_radius, int):
            self.__border_radius = border_radius
        else:
            raise TypeError(_TYPE_MSG("border_radius", border_radius, "int"))
        if isinstance(text_color, str):
            if re.match(_HEX_COLOR_PATTERN, text_color):
                self.__text_color = text_color
            else:
                raise ValueError(_VAL_MSG("text_color", text_color, "6-digit HEX value"))
        else:
            raise TypeError(_TYPE_MSG("text_color", text_color, "str"))
        if isinstance(disabled_color, str):
            if re.match(_HEX_COLOR_PATTERN, disabled_color):
                self.__disabled_color = disabled_color
            else:
                raise ValueError(_VAL_MSG("disabled_color", disabled_color, "6-digit HEX value"))
        else:
            raise TypeError(_TYPE_MSG("disabled_color", disabled_color, "str"))
        if isinstance(normal_color, str):
            if re.match(_HEX_COLOR_PATTERN, normal_color):
                self.__normal_color = normal_color
            else:
                raise ValueError(_VAL_MSG("normal_color", normal_color, "6-digit HEX value"))
        else:
            raise TypeError(_TYPE_MSG("normal_color", normal_color, "str"))
        if isinstance(click_color, str):
            if re.match(_HEX_COLOR_PATTERN, click_color):
                self.__click_color = click_color
            else:
                raise ValueError(_VAL_MSG("click_color", click_color, "6-digit HEX value"))
        else:
            raise TypeError(_TYPE_MSG("click_color", click_color, "str"))

        if self.__state == _NORMAL:
            self.__button_color = self.__normal_color
        else:
            self.__button_color = self.__disabled_color
        self.__pressed = False
        self.__function_executed = False
        
        if image is None:
            self.__image = None
        else:
            self.__image = self.__create_image_surface(image)
        
    def __create_image_surface(self, image):
        if isinstance(image, str):
            im_path = Path(image)
            if not im_path.exists() or not im_path.is_file():
                return None
            return pygame.image.load(image).convert_alpha()
        elif isinstance(image, PosixPath | WindowsPath):
            if not image.exists() or not image.is_file():
                return None
            return pygame.image.load(str(image)).convert_alpha()
        elif isinstance(image, pygame.Surface):
            return image.convert_alpha()
        else:
            return None

    def place(self, x: int, y: int, width: int, height: int):
        """Place button on Surface

        Args:
            x (int): Position on x-axis
            y (int): Position on y-axis
            width (int): Button's width
            height (int): Button's height
        """
        if not self.__image is None:
            self.__image = pygame.transform.scale(self.__image, (width, height)).convert_alpha()
        self.__top_rect = pygame.Rect((x, y), (width, height))
        self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
        self.__text_rect = self.__text_surface.get_rect(topleft=self.__top_rect.topleft)
        self.__text_rect.center = self.__top_rect.center
        pygame.draw.rect(self.__screen, self.__button_color, self.__top_rect,
                         border_radius=self.__border_radius)
        if not self.__image is None:
            im_rect = self.__text_surface.get_rect(topleft=self.__top_rect.topleft)
            self.__screen.blit(self.__image, im_rect)
        self.__screen.blit(self.__text_surface, self.__text_rect)
        self.__check_click()

    def config(self, text: str | None = ...,
               font: pygame.font.Font | None = ...,
               command: Callable[[], Any] | str = ...,
               args: list | tuple | None = ...,
               border_radius: int | None = ...,
               state: Literal["normal", "disabled"] = ...,
               text_color: str = ...,
               disabled_color: str = ...,
               normal_color: str = ...,
               click_color: str = ...):
        """Configure button attributes

        Args:
            text (str | None, optional): Change button text. Optional
            font (pygame.font.Font | None, optional): Change button font. Optional
            command (Callable[[], Any] | str, optional): Change command called. Optional
            args (list | tuple): Change command's argument list
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
            if self.__state == _NORMAL:
                self.__button_color = self.__normal_color
            elif self.__state == _DISABLED:
                self.__button_color = self.__disabled_color
        if isinstance(args, tuple | list):
            self.__args = tuple(args)
        if isinstance(border_radius, int) and border_radius >= 0:
            self.__border_radius = border_radius
        if isinstance(text_color, str) and re.match(_HEX_COLOR_PATTERN, text_color):
            self.__text_color = text_color
        if isinstance(disabled_color, str) and re.match(_HEX_COLOR_PATTERN, disabled_color):
            self.__disabled_color = disabled_color
        if isinstance(normal_color, str) and re.match(_HEX_COLOR_PATTERN, normal_color):
            self.__normal_color = normal_color
        if isinstance(click_color, str) and re.match(_HEX_COLOR_PATTERN, click_color):
            self.__click_color = click_color

    def __check_click(self):
        """Check button click
        """
        if self.__state == _DISABLED:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.__top_rect.collidepoint(mouse_pos):
            return
        if pygame.mouse.get_pressed()[0]:
            if self.__image is None:
                self.__button_color = self.__click_color
            else:
                self.__image.set_alpha(100)
            self.__pressed = True
            wc = lambda: Thread(target=self.__wait_click).start()
            wc()
        else:
            wc = Thread(target=self.__wait_click)
            wc.start()
            wc.join()

    def __wait_click(self):
        if not self.__pressed:
            return
        elif any(pygame.mouse.get_pressed()):
            return
        elif self.__function_executed:
            return
        elif not any(pygame.mouse.get_pressed()) and not self.__function_executed:
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
            if self.__image is None:
                self.__button_color = self.__normal_color
            else:
                self.__image.set_alpha(255)