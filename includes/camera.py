"""Camera.py

A module for camera in Pygame
"""
import os
from pathlib import Path, PosixPath, WindowsPath
import pygame

try:
    from includes.constants import CAMERA_SPEED, ENTER
    from includes.constants import W, A, S, D
except ImportError:
    from constants import CAMERA_SPEED, ENTER
    from constants import W, A, S, D

class CameraGroup(pygame.sprite.Group):
    """CameraGroup
    Sprite group
    """
    def __init__(self, ground_surface: pygame.Surface | str | WindowsPath | PosixPath = ...,
                 limit_x_positive: int | None = None, limit_x_negative: int | None = None,
                 limit_y_positive: int | None = None, limit_y_negative: int | None = None,
                 camera_speed: int = CAMERA_SPEED,
                 key_binding: tuple | list = (W, A, S, D), reset_key: int | None = ENTER):
        """CameraGroup
        Camera for pygame

        Args:
            ground_surface (pygame.Surface | str | WindowsPath | PosixPath): Display for background
            limit_x_positive (int | None, optional): Max x (positive)
            limit_x_negative (int | None, optional): Max x (negative)
            limit_y_positive (int | None, optional): Max y (positive)
            limit_y_negative (int | None, optional): Max y (negative)
            camera_speed (int): Camera speed
            key_binding (tuple | list): Camera keybinding
                Format: (Up, Left, Down, Right)
                Example: (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
            reset_key (int): Key ID. Reset camera to default position.
                Example: pygame.K_RETURN
        """
        super().__init__()
        self.__display_surface = pygame.display.get_surface()

        self.__width = self.__display_surface.get_size()[0]
        self.__height = self.__display_surface.get_size()[1]

        self.__offset = pygame.math.Vector2()
        self.__limits = {
            "x_positive": None,
            "y_positive": None,
            "x_negative": None,
            "y_negative": None
        }

        self.__camera_rect = pygame.Rect(0, 0, self.__width, self.__height)

        if isinstance(camera_speed, int):
            self.__camera_speed = camera_speed
        else:
            self.__camera_speed = CAMERA_SPEED

        self.__ground_surface = None
        if isinstance(ground_surface, pygame.Surface):
            self.__ground_surface = ground_surface
        elif isinstance(ground_surface, str):
            path = Path(ground_surface)
            if os.path.exists(path):
                self.__ground_surface = pygame.image.load(ground_surface).convert_alpha()
        elif isinstance(ground_surface, WindowsPath | PosixPath):
            if os.path.exists(ground_surface):
                self.__ground_surface = pygame.image.load(str(ground_surface)).convert_alpha()
        if not self.__ground_surface:
            self.__ground_surface = pygame.Surface((0, 0))
        self.__ground_rect = self.__ground_surface.get_rect(topleft = (0,0))

        if isinstance(limit_x_positive, int):
            if limit_x_positive < 0:
                limit_x_positive = -1 * limit_x_positive
            self.__limits["x_positive"] = limit_x_positive
        if isinstance(limit_y_positive, int):
            if limit_y_positive > 0:
                limit_y_positive = -1 * limit_y_positive
            self.__limits["y_positive"] = limit_y_positive
        if isinstance(limit_x_negative, int):
            if limit_x_negative > 0:
                limit_x_negative = -1 * limit_x_negative
            self.__limits["x_negative"] = limit_x_negative
        if isinstance(limit_y_negative, int):
            if limit_y_negative < 0:
                limit_y_negative = -1 * limit_y_negative
            self.__limits["y_negative"] = limit_y_negative

        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.__key_binding = key_binding
            else:
                self.__key_binding = (W, A, S, D)
        else:
            self.__key_binding = (W, A, S, D)

        if isinstance(reset_key, int):
            self.__reset_key = reset_key
        else:
            self.__reset_key = None

    def focus(self, target: pygame.sprite.Sprite):
        if not isinstance(target, pygame.sprite.Sprite):
            print("camera.py: Can not focus on target that is not a sprite")
            return
        try:
            if not isinstance(target.rect, pygame.Rect):
                print("camera.py: Target's rect is not pygame.Rect")
                return
        except NameError:
            print("camera.py: Target does not have rect attribute")
            return
        self.__camera_rect.x = target.rect.centerx - int(self.__width / 2)
        self.__camera_rect.y = target.rect.centery - int(self.__height / 2)

    def keyboard_control(self, allow_vertical: bool = True, allow_horizontal: bool = True):
        """Keyboard control
        A function to control camera using keyboard

        Args:
            allow_vertical (bool, optional): _description_. Defaults to True.
            allow_horizontal (bool, optional): _description_. Defaults to True.
        """
        keys = pygame.key.get_pressed()
        if allow_horizontal:
            if keys[self.__key_binding[1]]:
                self.__camera_rect.x -= self.__camera_speed
            if keys[self.__key_binding[3]]:
                self.__camera_rect.x += self.__camera_speed

            if self.__limits["x_negative"] is not None:
                if self.__camera_rect.x < self.__limits["x_negative"]:
                    self.__camera_rect.x += self.__camera_speed
            if self.__limits["x_positive"] is not None:
                if self.__camera_rect.x > self.__limits["x_positive"]:
                    self.__camera_rect.x -= self.__camera_speed

        if allow_vertical:
            allow_down = True
            allow_up = True
            if self.__limits["y_negative"] is not None:
                if self.__camera_rect.y + self.__camera_speed > self.__limits["y_negative"]:
                    allow_down = False
                else:
                    allow_down = True
            if self.__limits["y_positive"] is not None:
                if self.__camera_rect.y - self.__camera_speed < self.__limits["y_positive"]:
                    allow_up = False
                else:
                    allow_up = True

            if keys[self.__key_binding[0]] and allow_up:
                self.__camera_rect.y -= self.__camera_speed
            if keys[self.__key_binding[2]] and allow_down:
                self.__camera_rect.y += self.__camera_speed

        if self.__reset_key and keys[self.__reset_key]:
            self.reset_position()

        self.__offset.x = self.__camera_rect.left
        self.__offset.y = self.__camera_rect.top
        
        
    def reset_position(self):
        self.__camera_rect.x = 0
        self.__camera_rect.y = 0

    def config(self, ground_surface: pygame.Surface | str | WindowsPath | PosixPath = ...,
               limit_x_positive: int | None = ..., limit_x_negative: int | None = ...,
               limit_y_positive: int | None = ..., limit_y_negative: int | None = ...,
               camera_speed: int = ...,
               key_binding: tuple | list = ..., reset_key: int | None = ...):
        """Camera configuration

        Args:
            ground_surface (pygame.Surface | str | WindowsPath | PosixPath): Change ground display
            limit_x_positive (int | None, optional): Change max x limit (+)
            limit_x_negative (int | None, optional): Change max x limit (-)
            limit_y_positive (int | None, optional): Change max y limit (+)
            limit_y_negative (int | None, optional): Change max y limit (-)
            camera_speed (int, optional): Change camera speed
            key_binding (tuple | list): Camera keybinding
                Format: (Up, Left, Down, Right)
                Example: (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
        """
        if isinstance(ground_surface, pygame.Surface):
            self.__ground_surface = ground_surface
        elif isinstance(ground_surface, str):
            path = Path(ground_surface)
            if os.path.exists(path):
                self.__ground_surface = pygame.image.load(ground_surface).convert_alpha()
        elif isinstance(ground_surface, WindowsPath | PosixPath):
            if os.path.exists(ground_surface):
                self.__ground_surface = pygame.image.load(str(ground_surface)).convert_alpha()

        if isinstance(limit_x_positive, int):
            if limit_x_positive < 0:
                limit_x_positive = -1 * limit_x_positive
            self.__limits["x_positive"] = limit_x_positive
        if isinstance(limit_y_positive, int):
            if limit_y_positive > 0:
                limit_y_positive = -1 * limit_y_positive
            self.__limits["y_positive"] = limit_y_positive
        if isinstance(limit_x_negative, int):
            if limit_x_negative > 0:
                limit_x_negative = -1 * limit_x_negative
            self.__limits["x_negative"] = limit_x_negative
        if isinstance(limit_y_negative, int):
            if limit_y_negative < 0:
                limit_y_negative = -1 * limit_y_negative
            self.__limits["y_negative"] = limit_y_negative

        if limit_x_positive is None:
            self.__limits["x_positive"] = None
        if limit_y_positive is None:
            self.__limits["y_positive"] = None
        if limit_x_negative is None:
            self.__limits["x_negative"] = None
        if limit_y_negative is None:
            self.__limits["y_negative"] = None

        if isinstance(camera_speed, int):
            self.__camera_speed = camera_speed

        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.__key_binding = key_binding

        if isinstance(reset_key, int):
            self.__reset_key = reset_key

    def custom_draw(self, allow_vertical: bool = True, allow_horizontal: bool = True):
        """custom draw
        Draw

        Args:
            allow_vertical (bool, optional): control vertical movement
            allow_horizontal (bool, optional): control horizontal movement
        """
        self.keyboard_control(allow_vertical, allow_horizontal)

        ground_offset = self.__ground_rect.topleft - self.__offset
        self.__display_surface.blit(self.__ground_surface, ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)
