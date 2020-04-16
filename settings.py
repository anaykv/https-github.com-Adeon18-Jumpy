# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'fonts/Amatic SC'
SAVES_FILE = 'Saves'
COIN_FILE = 'coins'
SPRITESHEET1 = 'spritesheet_jumper.png'

# Player properties
PLAYER_ACC = 0.5
PLAYER_FLY_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_FRICTION_ON_SNOW = -0.04
PLAYER_FRICTION_ON_SAND = -0.2
PLAYER_GRAV = 0.8
PLAYER_JUMP_V = 20

# Game properties
BOOST_POWER = 40
SCR_CHANGE_H = HEIGHT / 2 - 80
SCR_CHANGE_H_FLY = HEIGHT / 6 * 5
# Bubble properties
BUBBLE_SPEED = 15
BUBBLE_END_SCORE = 200
BUBBLE_ACC = 0.5
# Wings properties
WINGS_END_SCORE = 450
WING_SPEED = 11
# Pow properties
POW_SPAWN_RATIO = 7
# Cloud_bg properties
CLOUD_BG_SPAWN_RATIO = 6
# Cloud properties
CLOUD_SPAWN_RATIO = 3
# Coin properties
COIN_SPAWN_RATIO = 3
# Plat properties
MOVING_PLAT_SPAWN_RATIO = 11
# Jetpack properties
JETPACK_ACC = 1.5
JETPACK_DEACC = 0.5
JETPACK_END_SCORE = 500
JETPACK_SPEED = 30
# Flyman properties
FLYMAN_FREQ = 7500
FLYMAN_SPAWN_RATIO = 75
FLYMAN_SPAWN_SCORE = 50
# Spikey properties
SPIKEY_ACC = 1
SPIKEY_SPAWN_RATIO = 7
SPIKEY_FRAME_TIME = 155
# Wingman properties
WM_ACC_UP = -2
WM_ACC_DOWN = 1.5
WM_VEL = 0.14
WM_SPAWN_RATIO = 3
WM_FRAME_TIME = 70
# Sun properties
SUN_FREQ = 15000
SUN_SPAWN_RATIO = 25
SUN_SPAWN_SCORE = 780
SUN_VEL = 2
SUN_FRAME_CHANGE = 220
# Layers
PLATFORM_LAYER = 1
PLAYER_LAYER = 5
POW_LAYER = 2
JETPACK_LAYER = 6
MOB_LAYER = 3
CLOUD_LAYER = 0
# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 55,), (WIDTH / 2 - 100, HEIGHT * 3 / 4), (125, HEIGHT - 350), (280, 200), (175, 100),
                 (20, -50)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (68, 142, 249)
ALMOST_WHITE = (226, 246, 247)
BG_COLOR = LIGHTBLUE

# Time properties
SEC = 1000
MINUTE = SEC * 60
