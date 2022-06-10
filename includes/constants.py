"""Constants

A file store constants for project
"""
import pygame
import tkinter as tk


# Main
root = tk.Tk()
WM_DELETE_WINDOW = "WM_DELETE_WINDOW"

WIN_WIDTH = 600
WIN_HEIGHT = 700
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
GREEN = "#57bd1c"

root.destroy()

# GAME
WIN_WIDTH = 600
WIN_HEIGHT = 600
GAME_WIDTH = 700
GAME_HEIGHT = 675
FPS = 30
MULTIPLIER = max(1, FPS / 30)

# Button
NORMAL = "normal"
DISABLED = "disabled"

# COLOR
RED = "#c92a2a"
GREEN = "#139e0e"
LIGHT_BLUE = "#2942F8"
BLUE = "#143c99"
YELLOW = "#d9bf00"
BLACK = "#000000"
WHITE = "#ffffff"
DARK_GRAY = "#4a4a4a"
LIGHT_GRAY1 = "#9c9c9c"
LIGHT_GRAY2 = "#EcEcEc"
# Button.py constants
NORMAL_STATE = "#475F77"
DOWN_STATE = "#D74B4B"
DISABLED_STATE = "#9c9c9c"
BOTTOM_COLOR = "#354B5E"
# Entry.py constants
ENTRY_ACTIVE = "#1C86EE"
ENTRY_INACTIVE = "#8DB6CD"

# Lesson 4: Config.py constants
HEX_TO_RGB = lambda hex: tuple((int(hex[i:i+2], 16) for i in (0, 2, 4)))

# FNP 4: Label, Sprites
HEX_COLOR_PATTERN = "^#([0-9A-Fa-f]{3}){1,2}$"

# FNP Camera
CAMERA_SPEED = 30
ENTER = pygame.K_RETURN
W = pygame.K_w
A = pygame.K_a
S = pygame.K_s
D = pygame.K_d

# FNP Sprite
OBJECT_BASE_SPEED = 300
DEFAULT_FILL_COLOR = "#FFFFFF"
DEFAULT_SIZE = (100, 100)
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

# Height meter
HM_FILL_COLOR = "#000000"
HM_RECT_SIZE = (20, 5)