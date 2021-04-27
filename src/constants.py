# Screen info
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FRAME_RATE = 30

# Sprite speeds
PLAYER_SPEED = 150
DEMON_SPEED = 150
SCROLL_SPEED = 90
OBSTACLE_SPEED = SCROLL_SPEED

# Sprite FPS
DEFAULT_FPS = 8
PLAYER_FPS = DEFAULT_FPS
DEMON_FPS = DEFAULT_FPS

# Light values
DARKNESS = 235
LIGHT = 200
LIGHT_DIFF = DARKNESS - LIGHT
LIGHT_SIZE = 175

# Spawn info
DEMON_SPAWN_TIME = 2000
DEMON_MIN_SPAWN_DIST = 20
DEMON_MAX_SPAWN_DIST = 100
OBSTACLE_SPAWN_TIME = 2000
OBSTACLE_MIN_SPAWN_DIST = DEMON_MIN_SPAWN_DIST
OBSTACLE_MAX_SPAWN_DIST = DEMON_MAX_SPAWN_DIST