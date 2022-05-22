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
        self.display_surface = pygame.display.get_surface()

        width = self.display_surface.get_size()[0]
        height = self.display_surface.get_size()[1]

        self.offset = pygame.math.Vector2()
        self.limits = {
            "x_positive": None,
            "y_positive": None,
            "x_negative": None,
            "y_negative": None
        }

        self.camera_rect = pygame.Rect(0, 0, width, height)

        if isinstance(camera_speed, int):
            self.camera_speed = camera_speed
        else:
            self.camera_speed = CAMERA_SPEED

        self.ground_surface = None
        if isinstance(ground_surface, pygame.Surface):
            self.ground_surface = ground_surface
        elif isinstance(ground_surface, str):
            path = Path(ground_surface)
            if os.path.exists(path):
                self.ground_surface = pygame.image.load(ground_surface).convert_alpha()
        elif isinstance(ground_surface, WindowsPath | PosixPath):
            if os.path.exists(ground_surface):
                self.ground_surface = pygame.image.load(str(ground_surface)).convert_alpha()
        if not self.ground_surface:
            self.ground_surface = pygame.Surface((0, 0))
        self.ground_rect = self.ground_surface.get_rect(topleft = (0,0))

        if isinstance(limit_x_positive, int):
            if limit_x_positive < 0:
                limit_x_positive = -1 * limit_x_positive
            self.limits["x_positive"] = limit_x_positive
        if isinstance(limit_y_positive, int):
            if limit_y_positive > 0:
                limit_y_positive = -1 * limit_y_positive
            self.limits["y_positive"] = limit_y_positive
        if isinstance(limit_x_negative, int):
            if limit_x_negative > 0:
                limit_x_negative = -1 * limit_x_negative
            self.limits["x_negative"] = limit_x_negative
        if isinstance(limit_y_negative, int):
            if limit_y_negative < 0:
                limit_y_negative = -1 * limit_y_negative
            self.limits["y_negative"] = limit_y_negative

        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.key_binding = key_binding
            else:
                self.key_binding = (W, A, S, D)
        else:
            self.key_binding = (W, A, S, D)

        if isinstance(reset_key, int):
            self.reset_key = reset_key
        else:
            self.reset_key = None

    def keyboard_control(self, allow_vertical: bool = True, allow_horizontal: bool = True):
        """Keyboard control
        A function to control camera using keyboard

        Args:
            allow_vertical (bool, optional): _description_. Defaults to True.
            allow_horizontal (bool, optional): _description_. Defaults to True.
        """
        keys = pygame.key.get_pressed()
        if allow_horizontal:
            if keys[self.key_binding[1]]:
                self.camera_rect.x -= self.camera_speed
            if keys[self.key_binding[3]]:
                self.camera_rect.x += self.camera_speed

            if self.limits["x_negative"] is not None:
                if self.camera_rect.x < self.limits["x_negative"]:
                    self.camera_rect.x += self.camera_speed
            if self.limits["x_positive"] is not None:
                if self.camera_rect.x > self.limits["x_positive"]:
                    self.camera_rect.x -= self.camera_speed

        if allow_vertical:
            allow_down = True
            allow_up = True
            if self.limits["y_negative"] is not None:
                if self.camera_rect.y + self.camera_speed > self.limits["y_negative"]:
                    allow_down = False
                else:
                    allow_down = True
            if self.limits["y_positive"] is not None:
                if self.camera_rect.y - self.camera_speed < self.limits["y_positive"]:
                    allow_up = False
                else:
                    allow_up = True

            if keys[self.key_binding[0]] and allow_up:
                self.camera_rect.y -= self.camera_speed
            if keys[self.key_binding[2]] and allow_down:
                self.camera_rect.y += self.camera_speed

        if self.reset_key and keys[self.reset_key]:
            self.camera_rect.x = 0
            self.camera_rect.y = 0

        self.offset.x = self.camera_rect.left
        self.offset.y = self.camera_rect.top

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
            self.ground_surface = ground_surface
        elif isinstance(ground_surface, str):
            path = Path(ground_surface)
            if os.path.exists(path):
                self.ground_surface = pygame.image.load(ground_surface).convert_alpha()
        elif isinstance(ground_surface, WindowsPath | PosixPath):
            if os.path.exists(ground_surface):
                self.ground_surface = pygame.image.load(str(ground_surface)).convert_alpha()

        if isinstance(limit_x_positive, int):
            if limit_x_positive < 0:
                limit_x_positive = -1 * limit_x_positive
            self.limits["x_positive"] = limit_x_positive
        if isinstance(limit_y_positive, int):
            if limit_y_positive > 0:
                limit_y_positive = -1 * limit_y_positive
            self.limits["y_positive"] = limit_y_positive
        if isinstance(limit_x_negative, int):
            if limit_x_negative > 0:
                limit_x_negative = -1 * limit_x_negative
            self.limits["x_negative"] = limit_x_negative
        if isinstance(limit_y_negative, int):
            if limit_y_negative < 0:
                limit_y_negative = -1 * limit_y_negative
            self.limits["y_negative"] = limit_y_negative

        if limit_x_positive is None:
            self.limits["x_positive"] = None
        if limit_y_positive is None:
            self.limits["y_positive"] = None
        if limit_x_negative is None:
            self.limits["x_negative"] = None
        if limit_y_negative is None:
            self.limits["y_negative"] = None

        if isinstance(camera_speed, int):
            self.camera_speed = camera_speed

        if isinstance(key_binding, tuple | list):
            if len(set(key_binding)) == 4:
                self.key_binding = key_binding

        if isinstance(reset_key, int):
            self.reset_key = reset_key

    def custom_draw(self, allow_vertical: bool = True, allow_horizontal: bool = True):
        """custom draw
        Draw

        Args:
            allow_vertical (bool, optional): control vertical movement
            allow_horizontal (bool, optional): control horizontal movement
        """
        self.keyboard_control(allow_vertical, allow_horizontal)

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surface, ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
