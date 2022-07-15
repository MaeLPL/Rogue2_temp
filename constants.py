import pygame
from PIL import Image
import tcod
import os
pygame.mixer.init(22100, -16, 2, 32)


pygame.init()
## DIMENSIONS

GAME_WIDTH = 1280
GAME_HEIGHT = 720

CELL_WIDTH = 16
CELL_HEIGHT = 16


# MiniMap

MINI_x = 1120
MINI_y = 16
MINI_fog_frame = (MINI_x+64, MINI_y + 64)
MINI_map = (MINI_x, MINI_y)

## UI
right_ui = pygame.image.load('UI/right_ui.png')
ramka = pygame.image.load('images/ramka.png')
krycie = pygame.image.load('krycie.png')

# FPS LIMIT
GAME_FPS = 200

# MAPS
TEXT_DISPLAY ="TEST"

Map_L11 = Image.open('gred.png').convert("RGB")
Map_L22 = pygame.image.load('gred.png')

Map_L1 = Image.open('grid.png').convert("RGB")
Map_L2 = pygame.image.load('grid.png')

# map2_w, map2_h = Map_L22.get_size()
# map2_w, map2_h = Map_L2.get_size()

Map_BC_L1 = Image.open('lvl1.png').convert("RGB")
Map_BC_L1_mini = pygame.image.load('lvl1.png')
map2_w, map2_h = Map_BC_L1_mini.get_size()



MAP_WIDTH = map2_w+5
MAP_HEIGHT = map2_h+5

## FOV SETTINGS

TORCH_RADIUS = 4
FOV_LIGHT_WALLS = True
FOV_ALGO = tcod.FOV_BASIC

# COLORS DEFs

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_BLACK_A = (255, 255, 255,255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)

# BG
# COLOR_DEFAULT_BG = COLOR_GRAY
COLOR_DEFAULT_BG = COLOR_BLACK


# # FONTS
# FONT_DEBUG_MESSAGE = pygame.font.Font('data\joystix.ttf', 18)
# FONT_MESSAGE_TEXT = pygame.font.Font('data\joystix.ttf', 12)

# MESSAGE DEFAULTS
NUM_MESSAGES = 10


#############################
###        SPRITES        ###
#############################

## onMAP

# Map_related

S_WALL = pygame.image.load("data/wall.png")
S_WALL_EX = pygame.image.load("data/wall.png")
S_WALL_EX.fill ((80,90,100), special_flags=pygame.BLEND_RGBA_MULT)  # RGB Correction

S_FLOOR = pygame.image.load("data/floor.png")
S_FLOOR_EX = pygame.image.load("data/floor.png")
S_FLOOR_EX.fill ((80,90,100), special_flags=pygame.BLEND_RGBA_MULT)  # RGB Correction

# NPCs, monsters etc
S_ENEMY = pygame.image.load("data/enemy.png")
S_ENEMY_DEAD = pygame.image.load("data/enemy_dead.png")

# PLAYER Sprites
S_PLAYER_UP = pygame.image.load("data/P_UP.png")
S_PLAYER_DOWN = pygame.image.load("data/P_DOWN.png")
S_PLAYER_LEFT = pygame.image.load("data/P_LEFT.png")
S_PLAYER_RIGHT = pygame.image.load("data/P_RIGHT.png")

SZABLON_LOL = pygame.image.load("data/szablon2.png")
INV_ICON = pygame.image.load("UI/box_inv.png")


# PLAYER Sprite list
#S_PLAYER_ARROW = [S_PLAYER_UP,S_PLAYER_RIGHT,S_PLAYER_DOWN,S_PLAYER_LEFT] ## unused

## UI
IMG_Portrait1 = pygame.image.load("UI/Acwellan.png")
IMG_Portrait2 = pygame.image.load("images/eyeLolsmall.png") ## unused

## Crawler view

# Monsters
S_SHARGA = pygame.image.load("data/sharga.png")
S_SHARGA_DEAD = pygame.image.load("data/sharga_red.png") ## unused
S_BEHO_LOL = pygame.image.load("data/behoLol.png")
S_BEHO_LOL2 = pygame.image.load("data/behoLol2.png")
S_BEHO_ANIM = [S_BEHO_LOL, S_BEHO_LOL2]
S_BEHO_LOL_2 = pygame.image.load("data/behoLol_2.png")
S_BEHO_LOL_2_2 = pygame.image.load("data/behoLol_2_2.png")
S_BEHO_ANIM2 = [S_BEHO_LOL_2, S_BEHO_LOL_2_2]
# S_BEHO_LOL_m = pygame.transform.scale(S_BEHO_LOL,(400,400))
# S_BEHO_LOL_m = pygame.image.load("data/behoLol_2.png")
S_BEHO_LOL_m2 = pygame.Surface((S_BEHO_LOL.get_width(), S_BEHO_LOL.get_height()), flags=pygame.SRCALPHA)


# Objects
P_CHEST = pygame.image.load("data/chest_new.png")
# P_CHEST.set_colorkey(COLOR_WHITE)
P_CHESTi = pygame.image.load("data/chest2_new.png")
# P_CHESTi.set_colorkey(COLOR_WHITE)
# P_CHEST_DEAD = pygame.image.load("data/chest_d.png") ## unused
L_Wand = pygame.image.load("items/763-rod.png")
L_Wand_F = pygame.image.load("items/764-.png") ## unused
L_Sword_I = pygame.image.load("items/sword2.jpg") ## unused
L_Sword_F = pygame.image.load("items/broad_sword_of_fire.png")

#L_Sword_F = pygame.image.load("data/sharga_red.png")
L_Staff = pygame.image.load("items/staff.png")
L_Spell = pygame.image.load("items/700-Spell Book.png")
L_Spell_f =  pygame.image.load("items/701-.png") ## unused
L_Axe_f =  pygame.image.load("images/items_floor/axe.png")
L_Axe = pygame.image.load("images/items_inv/axe.png")
P_CHEST_M = pygame.image.load("map_sprites/chest_16x16.png")
I_SpellBook = pygame.image.load("items/Spellbook2.bmp")

P_Key = pygame.image.load("items/key.png")

UI_Fist = pygame.image.load("images/fist.png")

Weapon_name = ["Fist", "Sword","Blaster"] ## unused
Weapon_str = [10,100,666] ## unused
Weapons = {'Staff': 10, 'Sword': 100, "Book": 666}
# PLAYER SPRITES
# n/a

#############################
###         WALLS         ###
#############################

## FLOOR

floor1 = pygame.image.load('images/walls/floor1.png')
floor2 = pygame.image.load('images/walls/floor2.png')
G_Floor = [floor1, floor2]

## Ceiling

ceiling1 = pygame.image.load('images/walls/ceiling1.png')
ceiling2 = pygame.image.load('images/walls/ceiling2.png')

G_Ceiling = [ceiling1, ceiling2]

# EOTB1 Wall textures
wall1_left  = pygame.image.load('images/close_l.png') #
wall1_left_flip  = pygame.image.load('images/close_l_flip.png') #

wall2_left  = pygame.image.load('images/wall_x.png')#
wall2_left_flip  = pygame.image.load('images/wall_x_flip.png')#

wall3_left  = pygame.image.load('images/far_l.png')
wall3_left_flip  = pygame.image.load('images/far_l_flip.png')

wall1_right = pygame.image.load('images/close_r.png')#
wall1_right_flip = pygame.image.load('images/close_r_flip.png')#

wall2_right = pygame.image.load('images/wall_y.png') #
wall2_right_flip = pygame.image.load('images/wall_y_flip.png') #

wall3_right = pygame.image.load('images/far_r.png')
wall3_right_flip = pygame.image.load('images/far_r_flip.png')

# wall1_mid = pygame.image.load('walls/close_m.png')
wall1_mid = pygame.image.load('images/wall1.png')
wall11_mid = pygame.image.load('images/wall2.png')
wall1_flip = pygame.transform.flip(wall1_mid, True, False)
# walls_mid = [wall1_mid,wall2_mid]
wall2_mid = pygame.image.load('images/mid_m.png')
wall2_mid_flip = pygame.image.load('images/mid_m_flip.png')

wall3_mid = pygame.image.load('images/far_m.png')
wall3_mid_flip = pygame.image.load('images/far_m_flip.png')

door1_mid = pygame.image.load('walls/door_1.png')
door2_mid = pygame.image.load('walls/door_2.png')
door3_mid = pygame.image.load('walls/door_3.png')
door4_mid = pygame.image.load('walls/door_4.png')

wall_button_bc = pygame.image.load('images/wall_button.png')
wall_button_bc1 = pygame.image.load('images/wall_button_p.png')
wall_button_L = pygame.image.load('images/wall_button_L.png')

door1_o_mid = pygame.image.load('walls/door_open.png')
door_c = pygame.image.load('map_sprites/door1_c.png')
door_o = pygame.image.load('map_sprites/door1_o.png')
m_button = pygame.image.load('map_sprites/button.png')

alcove = pygame.image.load('walls2/p26.png')
# alcove = pygame.image.load('walls/alcove.png')

# POSITIONING

### LEFT  FAR / MID/ CLOSE / ZERO

# W_left_far = (65, 148) ## Unused
W_left_mid = (11, 109)
W_left_close = (8, 48)
W_left_zero = (8, 5)

### MID FAR / MID / CLOSE / ZERO
W_mid_far = (292, 152)
W_mid_mid = (220, 109)
W_mid_close = (113, 48)
W_mid_zero = (0, 0)

### RIGHT FAR / MID / CLOSE / ZERO

# W_right_far = (515, 152) ## Unused
W_right_mid = (516, 109)
W_right_close = (576, 48)
W_right_zero = (682, 5)

# W_right_right_far = (736, 364)
# W_left_left_far = (7, 364)



## WALLS ATTEMPT #2
#TODO

L_FAR_POS = (69, 152)
L_Walls = [wall3_mid, wall3_left,wall2_left,wall1_left]
L_Walls_flip = [wall3_mid_flip, wall3_left_flip, wall2_left_flip,wall1_left_flip]
L_Walls_Pos = [L_FAR_POS ,W_left_mid, W_left_close, W_left_zero]
L_Walls_flipper = [L_Walls,L_Walls_flip]

# R_Walls =
R_FAR_POS = (515, 152)

R_Walls = [wall3_mid, wall3_right, wall2_right,wall1_right]
R_Walls_flip = [wall3_mid_flip, wall3_right_flip, wall2_right_flip,wall1_right_flip]
R_Walls_Pos = [R_FAR_POS, W_right_mid, W_right_close,W_right_zero]
R_Walls_flipper = [R_Walls,R_Walls_flip]



# MID WALLS
M_Walls = [wall3_mid_flip, wall2_mid, wall1_mid,wall1_mid]
M_Walls_flip = [wall3_mid, wall2_mid_flip, wall1_flip]
M_Walls_Pos = [W_mid_far, W_mid_mid, W_mid_close, W_mid_zero]
M_Walls_flipper = [M_Walls, M_Walls_flip]

### MONSTER POSITION
I_Chest = (70, 130)
M_mid_monster = (153, 118)
M_mid2_monster = (253, 118)
M_mid_wall = (113, 48)

monsterX_Y = [(153, 118), (280, 180), (330, 200)]
monsterX_Y1 = [(-230, 118), (-50, 180), (40, 200)]
monsterX_Y2 = [(570, 118), (620, 180), (620, 200)]

doorX_Y = [(114, 46), (225, 120), (310, 150)]
doorX_Y1 = [(-456, 45), (-115, 120), (80, 153)]
doorX_Y2 = [(678, 45), (575, 120), (516, 155)]

buttonX_Y = [(360, 160), (370, 170), (385, 190)]
buttonX_Y1 = [(-100, 160), (50, 170), (200, 190)]
buttonX_Y2 = [(780, 160), (730, 170), (670, 190)]


side_buttonX_Y = [(360, 160), (370, 170), (385, 190)]
side_buttonX_Y1 = [(170, 140), (250, 170), (200, 190)]
side_buttonX_Y2 = [(780, 160), (730, 170), (670, 190)]
alcoves = [pygame.image.load('images/Alcove1.png'),pygame.image.load('images/Alcove2.png'),pygame.image.load('images/Alcove3.png'),]
alcoveCenter = [(0,0),(200,90),(260,140),(340,185)]
alcoveLeft = [(0,0),(200,90),(300,90),(400,100)]
alcoveRight = [(0,0),(200,90),(300,90),(400,100)]


## Items on ground

#Left

Item_L_self_x = 240
Item_L_self_y = 555
Item_ahead_x = 320
Item_ahead_y = 450
Item_L_self = (Item_L_self_x, Item_L_self_y)
Item_L_start = (Item_L_self_x + 40, Item_L_self_y - 55)


itemX_Y = [(290,570),(320,480),(350,360),(370,330)]
itemX_Y_Alc = [(290,400),(320,310),(350,290),(370,250)]
itemX_Y_L = [(-230,570),(-74,480),(75,360),(190,330)]
itemX_Y_R = [(840,570),(710,480),(630,360),(550,330)]

### OBJ SCALING
M_scale =[(400,400),(200,200),(100,100)]

Scaler = [1,0.6,0.3]
AlcoveScaler = [1,0.6,0.3]
itemScaler = [1,0.7,0.5,0.3]
Door_scaler = [1,0.6,0.38]
### DIRECTIONS

# L_directions = ["N","E","S","W"] # not used
L_controls_x = [0, -1, 0, 1]
L_controls_y = [1, 0, -1, 0]

P_controls_x = [0, 1, 0, -1]
P_controls_y = [-1, 0, 1, 0]

L_facing = [2, 3, 0, 1]
P_facing = [0, 1, 2, 3]


# IMAGES




thunder = [pygame.image.load('data/thunder.png')]
fire = pygame.image.load('data/fball.png')



# SOUNDS
soundFX = pygame.mixer.Sound  # simplify defining new sounds
swordFX = soundFX('SFX\\blunt.wav')   # when hitting monsters
step1 = soundFX('SFX\\step2.wav')       # when taking step
SFX_thunder = soundFX('SFX\\blast.wav')
door_open = soundFX('SFX\\door_open.wav')
door_close = soundFX('SFX\\door_close.wav')
key_lock = soundFX('SFX\\key_lock.wav')
wall_move = soundFX('SFX\\wall_move.wav')

### MOUSE
MouseX, MouseY = (pygame.mouse.get_pos())


###################
###             ###
### COORDINATES ###
###             ###
###################

test_dict = {'Monster': (1,10), 'Chest': 2}

# Door Button 1

D_button_x = [400, 450]
D_button_y = [320, 400]

# Wall Button 1

W_button_x = 360
W_button_y = 160


Player_array = [0,0,0,0,0,0,0,0] ## Unused

UI_Minimap_dist=[-3,-2,-1,0,1,2,3]

random_range = [-1,1,0]
Walls_pos = [M_Walls_Pos,R_Walls_Pos,L_Walls_Pos]
Walls_flippers = [M_Walls_flipper, R_Walls_flipper,L_Walls_flipper]



pCloud1 = pygame.image.load('images/spells/bl1.png')
pCloud2 = pygame.image.load('images/spells/bl2.png')
pCloud3 = pygame.image.load('images/spells/bl3.png')
pCloud4 = pygame.image.load('images/spells/bl4.png')
pCloud5 = pygame.image.load('images/spells/bl5.png')

poison = [pCloud1, pCloud2, pCloud3, pCloud4, pCloud5]

def screenie(surf):
    for num in range(0, 2001):
        if os.path.isfile(f'DevShot{num}.png'):
            continue
        elif not os.path.isfile(f'DevShot{num}.png'):
            pygame.image.save(surf, f'DevShot{num}.png')
            return (f'DevShot{num}.png saved')
        else:
            print("THIS SHOULD NOT PRINT# CHECK CODE")

def L1_secrets(x,y):
    if x == 15 and y == 19:
        return "wall_close"
    if x == 16 and y == 23:
        return "wall_open"
    if x == 27 and y == 14:
        return "door_open"