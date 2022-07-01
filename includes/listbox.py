"""Listbox

Aa module for creating ListBox in pygame
"""

import math
import time
import re
import enum
from typing import Any, Callable, Literal
from threading import Thread

import pygame
from pygame import Surface

_WHITE = "#FFFFFF"
_BLACK = "#111111"
_GRAY = "#8c8c8c"
_YELLOW = "#DDDD00"
_BLUE = "#00AAFF"
_RED = "#FF4444"
_GREEN = "#37c421"
_HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"
_TYPE_MSG = lambda name, param, exp: f"invalid type for {name}: {type(param)}. Expected: {exp}"
_VAL_MSG = lambda name, param, expect: f"invalid value for {name}: {param}. Expected: {expect}"

class ItemStatus(enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    SELECTED = "selected"
    DISABLED = "disabled"

class WidgetState(enum.Enum):
    NORMAL = "normal"
    DISABLED = "disabled"

def _type_check(names: list, *params, expected_types: list):
    for name, param, expected_type in zip(names, params, expected_types):
        if not isinstance(param, expected_type):
            raise TypeError(_TYPE_MSG(name, param, f"{expected_type}"))

def _color_check(names: list, params: list, expected_value: str):
    for name, param in zip(names, params):
        if not re.match(_HEX_COLOR_PATTERN, param):
            raise ValueError(_VAL_MSG(name, param, expected_value))

class _ListBoxItem:
    def __init__(self, name: str, command: Callable[[], Any] | str = ...,
                 args: tuple | list = ..., text: str = ...,
                 status: Literal["available", "unavailable", "selected", "disabled"] = "available"
                 ) -> None:
        self.__name = name
        self.__command = command
        if isinstance(args, list | tuple):
            self.__args = args
        else:
            self.__args = None
        self.__text = text
        self.__status = status
        self.__executed = False

    @property
    def name(self):
        return self.__name
    @property
    def text(self):
        return self.__text
    @property
    def status(self):
        return self.__status
    @name.setter
    def name(self, value: str):
        self.__name = value
    @text.setter
    def text(self, value: str):
        self.__text = value
    @status.setter
    def status(self, value: str):
        if value in ("available", "unavailable", "selected", "disabled"):
            self.__status = value

    def run_command(self, use_thread: bool = False, wait_join: bool = True,
                     is_lambda:bool = False):
        if not self.__executed and pygame.event.peek(pygame.MOUSEBUTTONUP):
            self.__executed = True
            if is_lambda and self.__args:
                self.__command(*self.__args)
                self.__status = ItemStatus.AVAILABLE.value
                self.__executed = False
                return
            elif is_lambda and not self.__args:
                self.__command()
                self.__status = ItemStatus.AVAILABLE.value
                self.__executed = False
                return
            if use_thread and self.__args and not wait_join:
                work = lambda: Thread(target=self.__command, args=tuple(self.__args)).start()
                work()
            elif not use_thread and self.__args:
                self.__command(*self.__args)
            elif use_thread and not self.__args and not wait_join:
                work = lambda: Thread(target=self.__command).start()
                work()
            elif not use_thread and not self.__args:
                self.__command()
            elif use_thread and self.__args and wait_join:
                work = Thread(target=self.__command, args=tuple(self.__args))
                work.start()
                work.join()
            self.__executed = False
        time.sleep(0.5)
        self.__status = ItemStatus.AVAILABLE.value

    def config(self, name = ..., command = ..., text = ..., status = ...):
        if isinstance(name, str):
            self.__name = name
        if callable(command):
            self.__command = command
        if isinstance(text, str):
            self.__text = text
        if isinstance(status, str):
            if status in ("available", "unavailable", "selected", "disabled"):
                self.__status = status
            else:
                print("Invalid status")

class Listbox:
    def __init__(self, master: Surface,
                 font: pygame.font.Font,
                 max_item: int,
                 item_height: int,
                 max_item_on_page: int,
                 state: Literal["normal", "disabled"] = "normal",
                 text_color: str = _WHITE,
                 bg_color: str = _GRAY,
                 available_color: str = _BLUE,
                 unavailable_color: str = _RED,
                 selected_color: str = _YELLOW,
                 selected_border_color: str = _YELLOW
        ) -> None:
        self.__run_checkers(master, font, max_item, max_item_on_page, item_height,
                            state, text_color, bg_color, available_color,
                            unavailable_color, selected_color, selected_border_color)
        _color_check(["text_color", "bg_color", "available_color", "unavailable_color",
                      "select_color", "selected_border_color"],
                     [text_color, bg_color, available_color, unavailable_color, selected_color,
                      selected_border_color],
                     "6-digit HEX value")

        self.__screen = master
        self.__font = font
        self.__max_item = max_item
        self.__max_item_on_page = max_item_on_page
        self.__item_height = item_height
        self.__state = state
        self.__text_color = text_color
        self.__bg_color = bg_color
        self.__available_color = available_color
        self.__unavailable_color = unavailable_color
        self.__selected_color = selected_color
        self.__selected_border_color = selected_border_color

        self.__items = []
        self.__first_index = 0
        self.__colors = {
            "available": self.__available_color,
            "unavailable": self.__unavailable_color,
            "selected": self.__selected_color,
            "disabled": "#9c9c9c"
        }

    def add_item(self, name: str = "", command: Callable[[], Any] = ...,
                 args: tuple | list = ..., text: str = "",
                 status: Literal["available", "unavailable", "selected",
                                 "disabled"] = "available"):
        item = _ListBoxItem(name, command, args, text, status)
        self.__items.append(item)

    def remove_item(self, name: str = ""):
        for item in self.__items:
            if item.name == name:
                self.__items.remove(item)

    def config_item(self, index: int, name: str = ..., command: Callable[[], Any] = ...,
                    text: str = ..., status: str = ...):
        self.__items[index].config(name, command, text, status)

    def place(self, x: int, y: int, width: int, height: int):
        """Place button on Surface

        Args:
            x (int): Position on x-axis
            y (int): Position on y-axis
            width (int): Listbox width
            height (int): Listbox height
        """
        self.__main_surface = pygame.Surface((width - 10, height - 10))
        self.__main_rect = pygame.Rect((x, y), (width, height))
        self.__max_item_on_page = math.floor(height / self.__item_height)

        self.__main_surface.fill(self.__bg_color)
        self.__text_rects = []
        self.__text_surfaces = []
        pygame.draw.rect(self.__screen, _BLACK, self.__main_rect)
        for index, item in enumerate(self.__items[self.__first_index:self.__max_item_on_page]):
            text_surface = self.__font.render(item.text, True, self.__text_color)
            display_rect = pygame.Rect(
                0,
                index * self.__item_height,
                width - 10,
                self.__item_height
            )
            collision_rect = pygame.Rect(
                (x, y + index * self.__item_height), (width, self.__item_height)
            )
            pygame.draw.rect(self.__main_surface, self.__colors[item.status], display_rect, 3)
            self.__text_rects.append(collision_rect)
            self.__text_surfaces.append(text_surface)
        self.__screen.blit(self.__main_surface, (x + 5, y + 5))
        for index, text_surface in enumerate(self.__text_surfaces):
            self.__screen.blit(
                text_surface,
                (
                    x+10,
                    int(3 + y + index * self.__item_height + text_surface.get_height() / 2)
                )
            )
        self.__check_click()

    def __check_click(self):
        """Check button click
        """
        if self.__state == WidgetState.DISABLED:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]:
            return
        if not any(rect.collidepoint(mouse_pos) for rect in self.__text_rects):
            return
        for rect, item in zip(self.__text_rects, self.__items):
            if not rect.collidepoint(mouse_pos):
                continue
            if not item.status == ItemStatus.AVAILABLE.value:
                return
            item.config(status=ItemStatus.SELECTED.value)
            if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
                wc = lambda: Thread(target=item.run_command).start()
                wc()

    def get_objects(self):
        return self.__items

    def __run_checkers(self, *params):
        _type_check(
            ["master", "font", "max_item", "item_height",  "max_item_on_page", "state",
             "text_color", "bg_color", "available_color", "unavailable_color", "selected_color",
             "selected_border_color"],
            *params,
            expected_types=[Surface, pygame.font.Font, int, int, int, str, str, str, str, str,
                            str, str]
        )