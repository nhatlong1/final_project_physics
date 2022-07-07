import time
from typing import Callable, Any
from threading import Thread

import numpy as np
import pygame
from pymunk.pygame_util import to_pygame, from_pygame

from projectile.includes.constants import SIZE

def after(time_value: int, command: Callable[[], Any] | str = ...,
          args: list | tuple = ..., use_thread_and_join: bool = True):
    time.sleep(time_value)
    pass_args = None
    if isinstance(args, tuple | list):
        pass_args = tuple(args)
    if use_thread_and_join:
        if pass_args:
            th = Thread(target=command, args=pass_args)
        else:
            th = Thread(target=command)
        th.start()
        th.join()
    else:
        if pass_args:
            command(*pass_args)
        else:
            command()
            
def blur_screen(screen: pygame.Surface, strength: int | str = ..., color: str = "#7A7A7A"):
    if color.startswith("#"):
        color = color[1:]
    if isinstance(strength, int):
        strength = hex(strength)[2:]
    blur = pygame.Surface(SIZE, pygame.SRCALPHA)
    blur.fill(rf"#{color}{strength[:2]}")
    screen.blit(blur, (0, 0))
        
def pg_coord(tuple1, tuple2, surface, operation="-"):
    """Return a new tuple as pygame coordinates.

    Args:
        tuple1: First tuple
        tuple2: Second tuple
        surface: Surface
        operation (str): Operation. Defaults to "-", available: "+", "-"
    """
    if operation == "+":
        return to_pygame(tuple(np.add(tuple1, tuple2)), surface)
    else:
        return to_pygame(tuple(np.subtract(tuple1, tuple2)), surface)
    
def pm_coord(tuple1, tuple2, surface, op="-"):
    """Return a new tuple as pymunk coordinates.

    Args:
        tuple1: First tuple
        tuple2: Second tuple
        surface: Surface
        operation (str): Operation. Defaults to "-", available: "+", "-"
    """
    if op == "+":
        return from_pygame(tuple(np.add(tuple1, tuple2)), surface)
    else:
        return from_pygame(tuple(np.subtract(tuple1, tuple2)), surface)

def get_offset(camera):
    return (camera.x_offset, camera.y_offset)

def toggle_buttons(state: str = "normal", *buttons):
    for button in buttons:
        button.config(state=state)
