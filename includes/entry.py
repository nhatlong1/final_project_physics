"""Entry

A module for Entry in pygame
"""

import re
from threading import Thread
from typing import Any, Callable, Literal
import pygame

ENTRY_ACTIVE = "#1C86EE"
ENTRY_INACTIVE = "#8DB6CD"
HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{6})|#([0-9AFa-f]{8})"

class Entry:
    """Entry
    Entry class for pygame
    """
    def __init__(self, master: pygame.Surface, font: pygame.font.Font,
                 text: str | None = "", active: Literal[True, False] = False,
                 expand_max: int | None = None, command: Callable[[], Any] | str = ...,
                 max_len: int | None = None, clear_on_focus: bool = False,
                 regex_filter: str | None = None,
                 border_width: int = 1, border_radius: int = -1, active_color: str = ENTRY_ACTIVE,
                 border_color: str = ENTRY_INACTIVE, fg: str = "#000000", bg: str = "#FFFFFF",
                 state: Literal["normal", "disabled"] = "normal") -> None:
        """Entry

        Args:
            master (pygame.Surface): Surface to draw on
            font (pygame.font.Font): Font for text rendering
            text (str | None, optional): Init text.
            active (Literal[True, False], optional): Init state. Defaults to False.
            expand_max (int | None, optional): Max width expansion.
            command (Callable[[], Any] | str, optional):
                Command to call when RETURN key is pressed.
            max_len (int | None, optional): max input length.
            clear_on_focus (bool, optional): Clear entry field on select
            regex_filter (str, None, optional): A pattern to match input. If input does not
            match this pattern, input will be ignored
            border_width (int | None, optional): border width.
            border_radius (int | None, optional): border roundness.
            active_color (str): border color when entry is active
            border_color (str): border color when entry is inactive
            fg (str, optional): text color
            bg (str, optional): background color
            state (Literal["normal", "disabled"]): entry state
        """
        self._cleared_inputs = []
        self.recently_cleared = ""
        if master and isinstance(master, pygame.Surface):
            self.__screen = master
        elif not isinstance(master, pygame.Surface):
            raise TypeError("master must be a Surface")
        if text and isinstance(text, str):
            self.__text = f"{text}"
        else:
            self.__text = ""
        if font and isinstance(font, pygame.font.Font):
            self.__font = font
        elif not isinstance(font, pygame.font.Font):
            raise TypeError("font must be pygame.font.Font")
        if expand_max and isinstance(expand_max, int):
            self.__expand_max = expand_max
        elif expand_max is None:
            self.__expand_max = None
        else:
            raise TypeError(f"invalid type for expand_max: {type(expand_max)}. Expected: int")
        if callable(command):
            self.__command = command
        else:
            self.__command = lambda: None
        if isinstance(active, bool):
            self.__active = active
        else:
            raise TypeError(f"invalid type for active: {type(active)}. Expected: bool")
        if isinstance(max_len, int):
            self.__max_len = max_len
        elif max_len is None:
            self.__max_len = None
        else:
            raise TypeError(f"invalid type for max_len: {type(max_len)}. Expected: int or None")
        if isinstance(clear_on_focus, bool):
            self.__clear_on_focus = clear_on_focus
        else:
            raise TypeError(f"invalid type for clear_on_focus: {type(clear_on_focus)}. "
                            "Expected: bool")
        if isinstance(regex_filter, str):
            self.__regex_pattern = regex_filter
        elif regex_filter is None:
            self.__regex_pattern = None
        else:
            raise TypeError(f"invalid type for regex_filter: {type(regex_filter)}. "
                            "Expected: str, None")
        if isinstance(border_width, int):
            self.__border_width = border_width
        else:
            raise TypeError(f"invalid type for border_width: {type(border_width)}. Expected: int")
        if isinstance(border_radius, int):
            self.__border_radius = border_radius
        else:
            raise TypeError(f"invalid type for border_radius: {type(border_radius)}. Expected: int")
        if isinstance(active_color, str):
            if (re.match(HEX_COLOR_PATTERN, active_color)):
                self.__active_color = active_color
            else:
                raise ValueError(f"invalid value {active_color} for active_color")
        else:
            raise TypeError(f"invalid type for active_color: {type(active_color)}. Expected: str")
        if isinstance(border_color, str):
            if (re.match(HEX_COLOR_PATTERN, border_color)):
                self.__border_color = border_color
            else:
                raise ValueError(f"invalid value {border_color} for border_color")
        else:
            raise TypeError(f"invalid type for border_color: {type(border_color)}. Expected: str")
        if isinstance(state, str):
            if state.lower() in ("normal", "disabled"):
                self.__state = state.lower()
            else:
                raise ValueError(f"invalid value for state: {state}. Expected: \"normal\" or "
                                 "\"disabled\"")
        else:
            raise TypeError(f"invalid type for state: {type(state)}. Expected: str")
        if isinstance(fg, str):
            if re.match(HEX_COLOR_PATTERN, fg):
                self.__fg = fg
            else:
                raise ValueError(f"invalid value for fg: {fg}. Expected: 6-digit valid HEX color code")
        else:
            raise TypeError(f"invalid type for fg: {type(fg)}. Expected: str")
        if isinstance(bg, str):
            if re.match(HEX_COLOR_PATTERN, bg):
                self.__bg = bg
            else:
                raise ValueError(f"invalid value for bg: {bg}. Expected: 6-digit valid HEX color code")
        else:
            raise TypeError(f"invalid type for bg: {type(bg)}. Expected: str")
        self.__entry_rect = None

    def config(self, text: str | None = ..., font: pygame.font.Font | None = ...,
               active: Literal[True, False] = ..., expand_max: int | None = ...,
               max_len: int | None = ..., clear_on_focus: bool | None = ...,
               border_width: int | None = ..., border_radius: int | None = ...,
               active_color: str = ..., fg: str = ..., bg: str = ...,
               border_color: str = ..., state: Literal["normal", "disabled"] = ...) -> None:
        """Configure Entry attributes

        Args:
            text (str | None, optional): Text.
            font (pygame.font.Font | None, optional): Change font.
            active (Literal[True, False], optional): Change state.
            expand_max (int | None, optional): Change max expansion.
            max_len (int | None, optional): Change max length.
            clear_on_focus (bool | None, optional): Clear entry field on focus
            border_width (int | None, optional): Change border width
            border_radius (int | None, optional): Change border roundness
            active_color (str): Change active color
            border_color (str): Change border color
        """
        if isinstance(text, str):
            self.__text = f"{text}"
        if isinstance(font, pygame.font.Font):
            self.__font = font
        if isinstance(active, bool):
            self.__active = active
        if isinstance(expand_max, int):
            self.__expand_max=expand_max
        if isinstance(max_len, int):
            self.__max_len = max_len
        if isinstance(clear_on_focus, bool):
            self.__clear_on_focus = clear_on_focus
        if isinstance(border_radius, int):
            self.__border_radius = border_radius
        if isinstance(border_width, int):
            self.__border_width = border_width
        if isinstance(active_color, str) and re.match(HEX_COLOR_PATTERN, active_color):
            self.__active_color = active_color
        if isinstance(border_color, str) and re.match(HEX_COLOR_PATTERN, border_color):
            self.__border_color = border_color
        if isinstance(state, str):
            if state in ("normal", "disabled"):
                self.__state = state.lower()
        if isinstance(fg, str) and re.match(HEX_COLOR_PATTERN, fg):
            self.__fg = fg
        if isinstance(bg, str) and re.match(HEX_COLOR_PATTERN, bg):
            self.__bg = bg

    def place(self, x: int, y: int, width: int, height: int):
        """Place widget on screen

        Args:
            x (int): Position on x-axis
            y (int): Position on y-axis
            width (int): Entry width
            height (int): Entry height
        """
        self.__entry_rect = pygame.Rect((x, y), (width, height))
        self.__text_surface = self.__font.render(self.__text, True,
                                                 self.__fg, self.__bg)
        if self.__text_surface.get_width() > self.__entry_rect.width - 5:
            if self.__expand_max:
                self.__entry_rect.width = min(self.__text_surface.get_width() + 5, self.__expand_max)
                if self.__text_surface.get_width() > self.__expand_max - 5:
                    self.__text = self.__text[:-1]
            else:
                self.__text = self.__text[:-1]
        if self.__active:
            rect_color = self.__active_color
        else:
            rect_color = self.__border_color
        pygame.draw.rect(self.__screen, rect_color, self.__entry_rect, self.__border_width, border_radius=self.__border_radius)
        self.__screen.blit(self.__text_surface,
                         (x+5, y + int(height/2 - self.__text_surface.get_height()/2)))

    def handle_entry_events(self, event):
        if self.__state != "normal":
            print("State is not normal")
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__entry_rect.collidepoint(event.pos):
                if self.__clear_on_focus:
                    self.__text = ""
                self.__active = not self.__active
            else:
                self.__active = False
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.__command:
                        Thread(target=self.__command).start()
                    self._cleared_inputs.append(self.__text)
                    self.recently_cleared = self.__text
                    self.__text = ""
                else:
                    if self.__regex_pattern:
                        if not re.match(self.__regex_pattern, event.unicode):
                            return
                    if not self.__max_len is None:
                        if len(self.__text) < self.__max_len:
                            self.__text += event.unicode
                    else:
                        self.__text += event.unicode

    def get_status(self):
        return self.__active

    def get(self, do_clear_input: bool = True, as_type: type = str):
        """Get entry text

        Returns:
            str: Text from entry
        """
        if not isinstance(as_type, type):
            raise TypeError("Unexpected type for as_type. Expected: a valid type")
        return_text = self.__text
        if do_clear_input is True:
            self.__text = ""
        return as_type(return_text)

    def set(self, set_text: str = ...) -> None:
        """Set entry text
        """
        if isinstance(set_text, str):
            self.__text = set_text
