"""
Constants for Point of No Return
"""

import pygame_menu.themes
from pygame import locals

# Screen info
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FRAME_RATE = 60

# Menu constants
GAME_THEME = pygame_menu.themes.THEME_DARK.copy()
GAME_THEME.title_font = pygame_menu.font.FONT_8BIT
GAME_THEME.title_close_button = False

# Media constants
IMAGE_FOLDER = '../media/images'
AUDIO_FOLDER = '../media/audio'

# Sprite speeds
PLAYER_SPEED = 150
DEMON_SPEED = 150
SCROLL_SPEED = 90
OBSTACLE_SPEED = SCROLL_SPEED

# Sprite healths
PLAYER_HEALTH = 5
DEMON_HEALTH = 2
HEALTH_BAR_COLOR = (0, 100, 0)
HEALTH_BAR_UNIT_WIDTH = 40
HEALTH_BAR_HEIGHT = 15
HEALTH_BAR_POS = (15, 15)

# Sprite invincibility times in seconds
DEFAULT_INVINCIBILITY = 1
PLAYER_INVINCIBILITY = DEFAULT_INVINCIBILITY
DEMON_INVINCIBILITY = DEFAULT_INVINCIBILITY
TRANSPARENT_TIME = 1/6
INVINCIBILITY_ALPHA = 100

# Sprite knockback times (in seconds) and distances
DEFAULT_KNOCKBACK_TIME = 0.25
DEFAULT_KNOCKBACK_DIST = 70
PLAYER_KNOCKBACK_DIST = DEFAULT_KNOCKBACK_DIST
DEMON_KNOCKBACK_DIST = DEFAULT_KNOCKBACK_DIST

# Light values
DARKNESS = 230
LIGHT = 200
LIGHT_DIFF = DARKNESS - LIGHT
LIGHT_SIZE = 175

# Spawn info
DEMON_SPAWN_TIME = 3000
DEMON_MIN_SPAWN_DIST = 20
DEMON_MAX_SPAWN_DIST = 100
OBSTACLE_SPAWN_TRIGGER_DIST = SCREEN_HEIGHT/2 - 100
OBSTACLE_MIN_SPAWN_DIST = 50
OBSTACLE_MAX_SPAWN_DIST = 200

# Controls
MOVES = {
    'up': locals.K_w,
    'down': locals.K_s,
    'left': locals.K_a,
    'right': locals.K_d,
    'attack': locals.K_SPACE,
    'attack_up': locals.K_UP,
    'attack_down': locals.K_DOWN,
    'attack_left': locals.K_LEFT,
    'attack_right': locals.K_RIGHT,
}
