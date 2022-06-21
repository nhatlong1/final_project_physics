"""Sprites

A module for sprite in this project
"""

import os
import re
from pathlib import Path, WindowsPath, PosixPath
import pygame

try:
    from includes.constants import OBJECT_BASE_SPEED, DEFAULT_FILL_COLOR, DEFAULT_SIZE, \
        UP, DOWN, LEFT, RIGHT, HEX_COLOR_PATTERN, HM_FILL_COLOR, HM_RECT_SIZE
except ImportError:
    OBJECT_BASE_SPEED = 300
    DEFAULT_FILL_COLOR = "#FFFFFF"
    DEFAULT_SIZE = (100, 100)
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"
    HM_FILL_COLOR = "#000000"
    HM_RECT_SIZE = (20, 5)
    
    
class Forbidden(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FallObject(pygame.sprite.Sprite):
    """FallObject
    Originally a player sprite. Just change the name.
    """
    def __init__(self, pos: tuple, group: pygame.sprite.Group,
                 image: pygame.Surface | str | WindowsPath | PosixPath = ...,
                 constraint: bool = False, constraints: tuple | list = ...,
                 fill_color: str = DEFAULT_FILL_COLOR, rect_size: tuple = DEFAULT_SIZE,
                 movement_speed: int = OBJECT_BASE_SPEED,
                 allow_keyboard_control: bool = True,
                 key_binding: tuple | list = (UP, LEFT, DOWN, RIGHT)):
        """FallObject
        For FreeFall simulation. This thing will fall.

        Args:
            pos (tuple): position, (x, y)
            group (pygame.sprite.Group): group
            image (pygame.Surface | str | WindowsPath | PosixPath, optional): display image
            constraint (bool, optional): Do this sprite need to respect screen constraints.
            Defaults to False.
            constraints (tuple | list): Must be specified if constraint is True. Otherwise ignored.
                Format: (left, right, top, bottom)
            fill_color (str): Fill color when image load fail
            rect_size (tuple): A rectangle represent the player when image load fail
            movement_speed (int): Player move speed
            allow_keyboard_control (bool): Turn keyboard control on or off
            key_binding (tuple | list): 4 exclusive keys for directional movement
                Format: (Up, Left, Down, Right)
                Example: (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
            border_radius (int): Make corners rounder
        """
        super().__init__(group)
        self.image = None
        self.__constraint_flag = False
        if isinstance(image, str):
            path = Path(image)
            if os.path.exists(path):
                self.image = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image
        elif isinstance(image, WindowsPath | PosixPath):
            if os.path.exists(image):
                self.image = pygame.image.load(str(image)).convert_alpha()
        if not self.image:
            self.image = pygame.Surface(rect_size)
            self.image.fill(fill_color)
        if isinstance(constraint, bool):
            self.__constraint_flag = constraint

        if self.__constraint_flag and not isinstance(constraints, tuple | list):
            raise ValueError(
                f"inappropriate value for constraints when constraint is True: {constraints}")
        elif self.__constraint_flag and isinstance(constraints, tuple | list):
            tmp = list(constraints)
            if tmp[2] > 0:
                tmp[2] = -1 * tmp[2]
                constraints = tuple(tmp)
            self.__constraints = constraints
        if isinstance(movement_speed, int):
            self.__speed = movement_speed
        else:
            self.__speed = OBJECT_BASE_SPEED

        if isinstance(allow_keyboard_control, bool):
            self.__allow_keyboard_control = allow_keyboard_control
        else:
            self.__allow_keyboard_control = True

        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.__key_binding = key_binding
            else:
                self.__key_binding = (UP, LEFT, DOWN, RIGHT)
        else:
            self.__key_binding = (UP, LEFT, DOWN, RIGHT)

        self.rect = self.image.get_rect(topleft = pos)

        self.__direction = pygame.math.Vector2()
        self.__position = pygame.math.Vector2(self.rect.topleft)
        
    @property
    def speed(self):
        return self.__speed
    
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position_setter(self, value):
        self.__position = value
    
    @speed.setter
    def speed_setter(self, value: int | float):
        self.__speed = value

    def input(self):
        """Movement

        Move sprite by arrow keys
        """
        keys = pygame.key.get_pressed()

        if keys[self.__key_binding[0]]:
            self.__direction.y = -1
        elif keys[self.__key_binding[2]]:
            self.__direction.y = 1
        else:
            self.__direction.y = 0

        if keys[self.__key_binding[3]]:
            self.__direction.x = 1
        elif keys[self.__key_binding[1]]:
            self.__direction.x = -1
        else:
            self.__direction.x = 0

    def config(self, image: pygame.Surface | str | WindowsPath | PosixPath = ...,
               constraint: bool = ..., constraints: tuple | list = ..., fill_color: str = ...,
               movement_speed: int = ..., allow_keyboard_control: bool = ...,
               key_binding: tuple | list = ...):
        """Config

        Args:
            image (pygame.Surface | str | WindowsPath | PosixPath, optional): display image
            constraint (bool, optional): Do this sprite need to respect screen constraints.
            Defaults to False.
            constraints (tuple | list): Must be specified if constraint is True. Otherwise ignored.
                Format: (left, right, top, bottom)
            fill_color (str): Fill color when image load fail
                Warning: Using fill_color will overwrite image
            movement_speed (int): Player move speed
            allow_keyboard_control (bool): Turn keyboard control on or off
            key_binding (tuple | list): 4 exclusive keys for directional movement
                Format: (Up, Left, Down, Right)
                Example: (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
        """
        if isinstance(image, str):
            path = Path(image)
            if os.path.exists(path):
                self.image = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image
        elif isinstance(image, WindowsPath | PosixPath):
            if os.path.exists(image):
                self.image = pygame.image.load(str(image)).convert_alpha()
        if isinstance(constraint, bool):
            self.__constraint_flag = constraint
        if isinstance(constraints, tuple | list):
            self.__constraints = constraints
        if isinstance(fill_color, str):
            if re.match(HEX_COLOR_PATTERN, fill_color):
                self.image.fill(fill_color)
        if isinstance(movement_speed, int):
            if movement_speed > 0:
                self.__speed = movement_speed
            else:
                self.__speed = -1 * movement_speed
        if isinstance(allow_keyboard_control, bool):
            self.__allow_keyboard_control = allow_keyboard_control
        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.__key_binding = key_binding

    def constraint(self):
        """constraint
        """
        if self.rect.left < self.__constraints[0]:
            self.rect.left = self.__constraints[0]
            self.__position.x = self.rect.x
        if self.rect.right > self.__constraints[1]:
            self.rect.right = self.__constraints[1]
            self.__position.x = self.rect.x
        if self.rect.top < self.__constraints[2]:
            self.rect.top = self.__constraints[2]
            self.__position.y = self.rect.y
        if self.rect.bottom > self.__constraints[3]:
            self.rect.bottom = self.__constraints[3]
            self.__position.y = self.rect.y

    def update(self, delta_time: float):
        """Update
        Update sprite

        Args:
            dt (float): deltatime
        """
        if self.__allow_keyboard_control:
            self.input()
            self.__position.x += self.__direction.x * self.__speed * delta_time
            self.__position.y += self.__direction.y * self.__speed * delta_time
            self.rect.x = round(self.__position.x)
            self.rect.y = round(self.__position.y)
        if self.__constraint_flag:
            self.constraint()
            
            
class BackgroundSprite(pygame.sprite.Sprite):
    """Background
    Background for pygame
    """
    def __init__(self, groups: pygame.sprite.Group,
                 image: pygame.Surface | str | PosixPath | WindowsPath):
        """init

        Args:
            groups (pygame.sprite.Group): pygame group
            image (pygame.Surface | str | PosixPath | WindowsPath): image for background
        """
        super().__init__(groups)
        
        self.image = None
        if isinstance(image, str):
            path = Path(image)
            if os.path.exists(path):
                self.image = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image
        elif isinstance(image, WindowsPath | PosixPath):
            if os.path.exists(image):
                self.image = pygame.image.load(str(image)).convert_alpha()
        if not image:
            raise ValueError("please provide a value for image")
        self.rect = self.image.get_rect(topleft = (0, 75))

#!: WIP
class HeightMeter(pygame.sprite.Sprite):
    """Bar

    Sprite for height meter
    """
    def __init__(self, pos: tuple, group: pygame.sprite.Group, origin: tuple,
                fill_color: str = HM_FILL_COLOR, rect_size: tuple = HM_RECT_SIZE,):
        """_summary_

        Args:
            pos (tuple): position
            group (pygame.sprite.Group): pygame group
            origin (tuple): origin position
            fill_color (str, optional): bar fill color
            rect_size (tuple, optional): bar size
        """
        super().__init__(group)
        if isinstance(pos, tuple):
            self.pos = pos
        else:
            raise TypeError(f"Invalid type for pos: {type(pos)}. Expected: tuple")
        if isinstance(origin, tuple):
            self.origin = origin
        else:
            raise TypeError(f"Invalid type for origin: {type(origin)}. Expected: tuple")
        if isinstance(fill_color, str):
            self.fill_color = fill_color
        else:
            raise TypeError(f"Invalid type for fill_color: {type(fill_color)}. Expected: str")
        if not re.match(HEX_COLOR_PATTERN, self.fill_color):
            raise ValueError(f"Invalid value for fill_color: {self.fill_color}. Expected: 6-digit"
                             "HEX value for a color")
        if isinstance(rect_size, tuple):
            self.size = rect_size
        else:
            raise TypeError(f"Invalid type for rect_size: {type(rect_size)}. Expected: tuple")

        self.rect = pygame.Surface(rect_size)
        self.rect.fill(self.fill_color)
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.topleft)