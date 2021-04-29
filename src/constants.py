# Screen info
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FRAME_RATE = 30

# Media constants
IMAGE_FOLDER = '../media/images'
AUDIO_FOLDER = '../media/audio'

# Sprite speeds
PLAYER_SPEED = 150
DEMON_SPEED = 150
SCROLL_SPEED = 90
OBSTACLE_SPEED = SCROLL_SPEED

# Sprite FPS
DEFAULT_FPS = 8
PLAYER_FPS = DEFAULT_FPS
DEMON_FPS = DEFAULT_FPS

# Sprite healths
PLAYER_HEALTH = 5
DEMON_HEALTH = 2

# Sprite invincibility times in seconds
DEFAULT_INVINCIBILITY = 1
PLAYER_INVINCIBILITY = DEFAULT_INVINCIBILITY
DEMON_INVINCIBILITY = DEFAULT_INVINCIBILITY

# Sprite knockback times (in seconds) and distances
DEFAULT_KNOCKBACK_TIME = 0.25
DEFAULT_KNOCKBACK_DIST = 70
PLAYER_KNOCKBACK_DIST = DEFAULT_KNOCKBACK_DIST
DEMON_KNOCKBACK_DIST = DEFAULT_KNOCKBACK_DIST

# Light values
DARKNESS = 235
LIGHT = 220
LIGHT_DIFF = DARKNESS - LIGHT
LIGHT_SIZE = 175

# Spawn info
DEMON_SPAWN_TIME = 3000
DEMON_MIN_SPAWN_DIST = 20
DEMON_MAX_SPAWN_DIST = 100
OBSTACLE_SPAWN_TIME = 2000
OBSTACLE_MIN_SPAWN_DIST = DEMON_MIN_SPAWN_DIST
OBSTACLE_MAX_SPAWN_DIST = DEMON_MAX_SPAWN_DIST
