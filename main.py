import pygame
import pygame.gfxdraw
import tcod
import os, sys
import random, time
import tcod.map


### for Imaging
import numpy as np
from PIL import Image

### pygame extras
pygame.mixer.init(44100, -16, 2, 512)
# pygame.mixer.init(22100, -16, 2, 32)

### Additional files
import constants
# import items

# Extra files used

######################################### STRUCTURE ###

class struc_Tile:
    def __init__(self, block_path, door_path = False, button_path = False, wall_alcove = False):
        self.block_path = block_path
        self.door_path = door_path
        self.button_path = button_path
        self.explored = False
        self.wall_alcove = wall_alcove
#

class struc_Assets:
    def __init__(self):
        self.SHEET_ONE = obj_SpriteSheet("sheets/sheet_2.png")
        self.SpellBook = pygame.image.load("UI/Spellbook2.bmp")
        self.Sword = pygame.image.load("UI/sword.bmp")
        #self.Door = pygame.image.load("map_sprites/door1.png")

        self.SpellBook_rect = self.SpellBook.get_rect()
        self.right_ui_pos = (801,19)
        self.right_ui_posx = 801
        self.right_ui_posy = 19
        self.right_ui_size = (463,684)

        self.hero_face = 886

        ##FONTS
        self.FONT_DEBUG_MESSAGE = pygame.font.Font('data\joystix.ttf', 24)
        self.FONT_MESSAGE_TEXT = pygame.font.Font('data\joystix.ttf', 12)


######################################### OBJECT ###
class obj_Actor:
    def __init__(self,x ,y, facing, name_object, sprite, crawl_sprite, sprite_anim,type, sprite_anim_far = None,
                 creature=None, ai= None, container = None, item = None, status=None, target_obj=None,
                 ):
        # x = ,
        # y = ,
        # facing = ,
        # name_object = "",
        # sprite = ,
        # crawl_sprite = ,
        # sprite_anim = ,
        # creature = ,# class
        # ai = ,# class
        # container = ,# class
        # item = ,# class

        self.x = x
        self.y = y
        self.facing = facing
        self.name_object = name_object
        self.sprite = sprite
        self.crawl_sprite = crawl_sprite
        self.sprite_anim = sprite_anim
        self.sprite_anim_far = sprite_anim_far
        self.creature = creature
        self.status = status
        self.target_obj = target_obj
        self.type = type

        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self
        self.item = item
        # if self.item:
        #     self.item.owner = self

    def draw(self):
        # top_right_map = (constants.GAME_WIDTH - 256)

        # is_visible = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        # if is_visible:
        #     SURFACE_MAIN.blit(self.sprite, (top_right_map + self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
        # left_map = 16
        is_visiblel = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visiblel:
            if self.creature.name_instance != "MaeL":
                # SURFACE_MAIN.blit(self.sprite,(((self.x - PLAYER.x)*16) +64, ((self.y - PLAYER.y)*16) +64))
                SURFACE_MAIN.blit(self.sprite,(
                                                constants.MINI_x+(((self.x - PLAYER.x)*16) +64),
                                                constants.MINI_y+ ((self.y - PLAYER.y)*16) +64))
            else:
                SURFACE_MAIN.blit(self.sprite,constants.MINI_fog_frame)

    def draw_on_map(self):
        window_width = constants.GAME_WIDTH
        window_height = constants.GAME_HEIGHT

        map_width = constants.map2_w * 16
        map_height = constants.map2_h * 16

        map_width_x = (window_width / 2) - (map_width / 2)
        map_height_y = (window_height / 2) - (map_height / 2)
        is_visiblel = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visiblel:
            SURFACE_MAIN.blit(self.sprite,(map_width_x+self.x*constants.CELL_WIDTH, map_height_y+self.y*constants.CELL_HEIGHT))

    def draw_self_fpp(self,distance):

        if (self.x + distance == PLAYER.x or self.x - distance == PLAYER.x) and self.y == PLAYER.y:
            if self.type == "Monster":
                self.crawl_sprite = self.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
                SURFACE_MAIN.blit((pygame.transform.scale(self.crawl_sprite,
                                                          (int(self.crawl_sprite.get_width() * constants.Scaler[distance-1]),
                                                           int(self.crawl_sprite.get_height() * constants.Scaler[distance-1])))),
                                  constants.monsterX_Y[distance-1])
            elif self.type == "Chest":
                print(self.type)
            # elif self.type == "Chest":
            #     print("PUDLO")
    # Mon_List = []
    # def draw_in_fpp(self, playerX, playerY):
    #
    #         SURFACE_MAIN.blit(self.crawl_sprite, constants.M_mid_monster)




#
# class obj_interactables:
#     def __init__(self,x ,y, facing, name_object, sprite, crawl_sprite, sprite_anim,
#                  creature=None,container = None, item = None, status = None, ai = None,
#                  target_obj = None):
#
#         self.x = x
#         self.y = y
#         self.facing = facing
#         self.name_object = name_object
#         self.sprite = sprite
#         self.crawl_sprite = crawl_sprite
#         self.sprite_anim = sprite_anim
#
#         self.creature = creature
#         if self.creature:
#             self.creature.owner = self
#
#         self.container = container
#         if self.container:
#             self.container.owner = self
#         self.item = item
#
#         # if self.item:
#         #     self.item.owner = self
#
#         self.status = status
#         # if self.status:
#         #     self.status.owner = self
#
#         self.ai = ai
#         self.target_obj = target_obj
#
#     def draw(self):
#         # top_right_map = (constants.GAME_WIDTH - 256)
#         local_surface = pygame.Surface((constants.GAME_WIDTH-(9*16), constants.GAME_HEIGHT-(9*16)))
#
#         is_visible = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
#         if is_visible:
#             SURFACE_MAIN.blit(self.sprite, (
#                 constants.MINI_x + (((self.x - PLAYER.x) * 16) + 64),
#                 constants.MINI_y + ((self.y - PLAYER.y) * 16) + 64))
#     def draw_on_map(self):
#         window_width = constants.GAME_WIDTH
#         window_height = constants.GAME_HEIGHT
#
#         map_width = constants.map2_w * 16
#         map_height = constants.map2_h * 16
#
#         map_width_x = (window_width / 2) - (map_width / 2)
#         map_height_y = (window_height / 2) - (map_height / 2)
#         is_visiblel = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)
#         if is_visiblel:
#             SURFACE_MAIN.blit(self.sprite,(map_width_x+self.x*constants.CELL_WIDTH, map_height_y+self.y*constants.CELL_HEIGHT))
#
#     def draw_in_fpp(self, playerX, playerY):
#             if ((playerX == self.x)
#                     and (playerY + 3 == self.y)):
#                 # new_gfx = (pygame.transform.scale(game_obj.crawl_sprite, (200, 200)))
#                 if self.creature.object_type == "DOOR":
#                     # SURFACE_MAIN.blit((pygame.transform.scale(game_obj.crawl_sprite, (100, 100))), (350, 200))
#                     SURFACE_MAIN.blit(self.crawl_sprite, constants.M_mid_monster)
#
#                 else:
#                     print("NOT PRINT, CHECK")
#
#             if ((PLAYER.x == self.x)
#                     and (PLAYER.y + 2 == self.y)):
#                 # new_gfx =( pygame.transform.scale(game_obj.crawl_sprite, (200,200)))
#                 if self.creature.object_type == "DOOR":
#                     # game_obj.crawl_sprite.convert_alpha()
#                     # SURFACE_MAIN.blit(( pygame.transform.scale(game_obj.crawl_sprite, (200,200))), (300,180))
#                     SURFACE_MAIN.blit(self.crawl_sprite, constants.M_mid_monster)
#
#                 else:
#                     print("NOT PRINT, CHECK")

class obj_Items:
    def __init__(self, x = None, y = None, name = "PlaceholderName",
                 type = "Typeless", power = 1, effect = None, weight = None,
                 i_sprite = "", f_sprite = ""):
        self.name = name
        self.type = type
        self.power = power

        self.x = x
        self.y = y
        self.effect = effect
        self.weight = weight
        self.i_sprite = i_sprite
        self.f_sprite = f_sprite

        # if self.x:
        #     self.x = self
        # if self.y:
        #     self.y = self
        if self.effect:
            self.effect.owner = self
        if self.weight:
            self.weight.owner = self

    def drop_down(self, new_x, new_y):
        GAME.interact_objects.append(self)

        self.container.inventory.remove(self)

        self.x = new_x
        self.y = new_y

        game_message(f'{self.name} dropped')

    def pick_op(self, actor):
        if actor.container:

            # game_message(f'{self.name} Picked up')
            # actor.container.inventory.append(self.owner)
            # GAME.current_objects.remove(self.owner)
            # self.container = actor.container
            game_message(f'{self.name} Picked up')

            actor.container.inventory.append(self)

            # actor.container.inventory.append(self.owner)
            # print(self.owner)

            for x in PLAYER.container.inventory:
                constants.Player_array = [1 if 0 else 0 for x in PLAYER.container.inventory]
                # constants.Player_array[x] = "1"
            GAME.interact_objects.remove(self)
            self.container = actor.container

    def unequip(self, new_x, new_y):
        # GAME.interact_objects.append(self)
        MOUSE.append(PLAYER.creature.gear)
        PLAYER.creature.gear = GAME_INTERACTS[0]
        self.x = new_x
        self.y = new_y

        game_message(f'{self.name} Unequipped', constants.COLOR_RED)

    def replace(self, old, new):
        temp = old
        PLAYER.creature.gear = new
        MOUSE.remove(new)
        MOUSE.append(old)

    def check_item(self, lock):

        constants.key_lock.play()
        if lock == self.name:
            game_message(f'{lock} used!', constants.COLOR_GREEN)
            MOUSE.remove(self)
            return True
        else:
            game_message(f'Wrong key, try using {lock}!', constants.COLOR_RED)
            # constants.key_lock.play()
    def equip(self, actor,item):
        if actor.creature.gear.name != "Fist":
            actor.creature.gear.unequip(PLAYER.x, PLAYER.y)
        actor.creature.gear = self
        game_message(f'{self.name} equipped', constants.COLOR_YELLOW)
        #
        # actor.creature.gear.i_sprite = self.i_sprite
        #
        # actor.creature.gear.power = self.power
        # actor.creature.gear.i_sprite = self.i_sprite

        # print(self.container.inventory[item].gear.name)

    def item_examine(self, slot):
        game_message(f'This is a {self.name} in slot #{slot}')
        return self.name

    ## MOUSE ACTIONS
    def mouse_pick_up(self, actor):

        game_message(f'{self.name} Picked up to pointer')
        actor.append(self)
        # for x in PLAYER.container.inventory:
        #     constants.Player_array = [1 if 0 else 0 for x in PLAYER.container.inventory]
        # constants.Player_array[x] = "1"

        GAME.interact_objects.remove(self)


    def mouse_drop(self, new_x, new_y):
        GAME.interact_objects.append(self)
        self.x = new_x
        self.y = new_y

        game_message(f'{self.name} dropped from pointer')
        MOUSE.remove(self)

class obj_Game:
    def __init__(self):
        #self.GAME.current_map = map_create()
        self.current_map = map_create()

        #self.GAME.current_objects = [ENEMY, PLAYER]
        self.current_objects = []

        self.next_lvl = []
        #self.GAME.message_history = []
        self.message_history = []

        self.interact_objects = []


class obj_SpriteSheet:
    '''grab images out of sprite sheets'''

    def __init__(self, file_name):
        # Load spritesheet
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8}
    ###########################################################

    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
                  scale= None):
        ''' scale is a tuple'''

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0),(self.tiledict[column]*width, row*height, width, height))

        image.set_colorkey(constants.COLOR_BLUE)

        if scale:
            (new_width, new_height) = scale
            image = pygame.transform.scale(image,(new_width,new_height))
        return image

class all_spells:

    def __init__(self, spell_name, spell_dmg, cooldown, isActive = True, cast_type = None, spell_sprite = None):
        self.spell_name = spell_name
        self.spell_dmg = spell_dmg
        self.cooldown = cooldown
        self.isActive = isActive
        self.cast_type = cast_type
        self.spell_sprite = spell_sprite

    # def spell_anim(self):


###############################################################

###                     COMPONENT                           ###

###############################################################

class com_Creature:
    '''
    hasHealth
    takeHit
    canAttack
    isAlive
    notNameless
    '''
    #test = 0
    def __init__(self, name_instance, object_type, hp = 10,death_function=None,
                 gear=None, crawl_sprite=None, type = None, portrait=None):
        self.name_instance = name_instance
        self.object_type = object_type
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function
        self.crawl_sprite = crawl_sprite

        self.gear = gear
        if gear:
            gear.owner = self
        self.type = type
        self.portrait = portrait

#TODO re-code attack function, add monster check to see if player nearby, roll for move or attack
    #TODO remove attack from move option

    def move(self, dx, dy):
        attacker_name = self.name_instance
        tile_is_wall   = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)
        tile_is_door   = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].door_path  == True)
        tile_is_button = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].button_path == True)
        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
        #if self.name_instance == PLAYER.creature.name_instance:
        if tile_is_door and self.owner == PLAYER:
            game_message("Try opening the door first!", constants.COLOR_RED)
        elif not tile_is_wall and not tile_is_door and (target is None or target.creature.type == "Door"):
            # if not self.object_type =="Monster":
            self.owner.x += dx
            self.owner.y += dy

            # else:
            #     print(f'NO ACTION TAKEN BY {self.owner.name_object}')
            #     # self.owner.facing += 1
            #     # print (self.owner.facing)
            if self.name_instance == PLAYER.creature.name_instance:
                constants.step1.play()
                if constants.L1_secrets(PLAYER.x, PLAYER.y) == "wall_close":
                    GAME.current_map[15][20].block_path = True
                    map_make_fov(GAME.current_map)

                elif constants.L1_secrets(PLAYER.x, PLAYER.y) == "wall_open":
                    GAME.current_map[15][20].block_path = False
                    map_make_fov(GAME.current_map)

                elif constants.L1_secrets(PLAYER.x, PLAYER.y) == "door_open":
                    target = map_check_for_creatures(26, 16, PLAYER)
                    door_helper(target, target.creature.type)
                    target.status = "door_opened"

        elif tile_is_door:
            if target.name_instance:
                game_message("Try opening the door first!", constants.COLOR_RED)
        elif target :
            if target.creature.type =="Alcove":
                game_message(f"There's a {target.creature.name_instance}! Loot it!", constants.COLOR_WHITE)
            elif target.creature.type != "Button" and target.creature.type != "Wall" and self.owner == PLAYER:
            # self.attack(target, self.gear.att)
            # print(target)
                game_message(f"There's a {target.creature.name_instance}! Better attack it!", constants.COLOR_WHITE)
            #FOV_CALCULATE = True
        elif tile_is_wall:
            if not target:
                if self.owner == PLAYER:
                    game_message(f"{self.owner.name_object} BUMPED into a wall!", constants.COLOR_RED)
            elif target.creature.type == "Button" and self.name_instance == "MaeL":
                game_message("Button! Press it!", constants.COLOR_WHITE)

            elif target.creature.type == "Wall":
                # game_message("This wall seems odd..", constants.COLOR_WHITE)
                print("remember to adjust monster AI")
        # elif tile_is_wall:
        #     if self.owner == PLAYER:

                 #self.wall_bump(self.owner.x,self.owner.y)
            # print("Path Blocked at x:" + str(self.owner.x) + ", y:" + str(self.owner.y))
        else:
            print("### THIS SHOULD NOT PRINT, CHECK CODE!@ ###")

    def attack(self,target, damage):
        game_message(f"{self.name_instance} hits for {damage} Damage", constants.COLOR_RED)
        target.creature.take_damage(damage)
        if self.name_instance == PLAYER.creature.name_instance:
            # print(self.creature.gear.name_weapon, "attacks", target.creature.name_instance)
            constants.swordFX.play()
            time.sleep(0.25)
    def atack(self, damage):
        target =map_check_for_creatures(self.owner.x - constants.L_controls_x[self.owner.facing],
                                        self.owner.y - constants.L_controls_y[self.owner.facing], self.owner)
        if target and not target.creature.type:
            game_message(self.name_instance + " hits " + target.creature.name_instance + " for " + str(damage) + " Damage", constants.COLOR_RED)
            target.creature.take_damage(damage)
            if self.name_instance == PLAYER.creature.name_instance:
                # print(self.creature.gear.name_weapon, "attacks", target.creature.name_instance)
                constants.swordFX.play()
                time.sleep(0.25)
        else:
            game_message("No Target", constants.COLOR_BLUE)

    def spellcast(self,dmg, type, sprite, spell_name):
        if type == "spellcast":
            draw_game()
            target = map_check_for_creatures(self.owner.x - constants.L_controls_x[self.owner.facing], self.owner.y - constants.L_controls_y[self.owner.facing], self.owner)

            if target and not target.creature.type:
                take_break = False
                game_message(str(self.name_instance + " casts " + spell_name + ". Dmg dealt:"+ str(dmg)),constants.COLOR_WHITE)
                target.creature.take_damage(dmg)
                # for repeats in range (0,3):
                constants.SFX_thunder.play()
                    # time.sleep(0.025)

                if sprite and len(sprite) >1:
                    spell_helper(sprite)
                else:
                    SURFACE_MAIN.blit(sprite[0], (30, 30))
                    take_break = True

                pygame.display.update()

                if take_break:
                    time.sleep(2.25)

                # pygame.display.update()
                # time.sleep(0.25)
            else:
                return "canceled"
        elif type == "self_heal":
            cast_heal(dmg,self.owner)



    def take_damage(self,damage):
        self.hp -= damage
        game_message(self.name_instance + " has " + str(self.hp) + "/"+ str(self.maxhp)+" hp left")

        if self.hp <= 0:

            if self.death_function is not None:

                self.death_function(self.owner)
                self.owner.sprite = constants.S_ENEMY_DEAD


    def heal(self,value):
        self.hp += value
        if self.hp >self.maxhp:
            self.hp = self.maxhp

    def wall_bump(self, x, y):
        print("Path Blocked at x:" + str(x) + ", y:" + str(y))


class com_Weapon:
    def __init__(self, name_weapon, att = 10):
        self.name_weapon = name_weapon
        self.att = att


###############################################################

###                     AI STUFF                            ###

###############################################################
class ai_Test:
    def patrol(self):
        m_x = tcod.random_get_int(0, -1, 1)  # random.randint(-1,1)
        m_y = tcod.random_get_int(0, -1, 1)  # random.randint(-1,1)
        self.owner.creature.move(m_x,m_y)

    def take_turn(self):
        skip = False
        if self.owner.creature and self.owner.name_object != "DOOR" :
            for y in range(-1,2):
                for x in range(-1,2):
                    if not skip:
                        if (self.owner.x + x == PLAYER.x and self.owner.y == PLAYER.y)\
                                or (self.owner.x == PLAYER.x and self.owner.y + y == PLAYER.y):
                            game_message("I HIT YOU@",constants.COLOR_RED)
                            skip = True
                        elif self.owner.x + x == PLAYER.x and self.owner.y + y == PLAYER.y:
                            game_message("I see you!")
                            skip = True
            if not skip:
                m_x = tcod.random_get_int(0, -1, 1)  # random.randint(-1,1)
                m_y = tcod.random_get_int(0, -1, 1)  # random.randint(-1,1)
                self.owner.creature.move(m_x, m_y)


class ai_Aggro:
    def take_turn(self):
        if self.owner.creature.name_instance == "Paint Monster":
            if (((self.owner.x - PLAYER.x == +1 or self.owner.x - PLAYER.x == -1) and self.owner.y == PLAYER.y) or
                ((self.owner.y - PLAYER.y == +1 or self.owner.y - PLAYER.y == -1) and self.owner.x == PLAYER.x)):
                if self.owner.facing == self.owner.creature.atack(PLAYER.creature.gear.att):
                    print ('yay')

class ai_PlaceHolder:
    def idle(self):
        pass

class ai_Doors:
    def take_turn(self):
        if self.owner.name_object == "DOOR":
            print(self.owner.x, self.owner.y)
            #GAME.current_map[self.owner.x][self.owner.y].door_path = True


def death_monster(monster):
    game_message(f'{monster.creature.name_instance} is ded')
    # if monster.item.f_sprite:
    #     monster.crawl_sprite = monster.item.f_sprite
    if monster.creature.gear:
        monster.creature.gear.x = monster.x
        monster.creature.gear.y = monster.y
        print(monster.creature.gear.name)
        GAME.interact_objects.append(monster.creature.gear)

    # monster.creature = None
    # monster.ai = None

    for obj in GAME.current_objects:
        if obj == monster:
            GAME.current_objects.remove(monster)


# TODO class com_Item:

# TODO class com_Container:


class com_Container:
    def __init__(self,volume = 10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume
    ## TODO get names of items in inv

    ## TODO get volume within container
    @property
    def volume(self):
        return 0.0
    ## TODO get weight of inventory

# class com_MouseContainer:
#     def __init__(self, inventory = []):
#         self.inventory = inventory


class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0, use_function=None, value=None,
                 name=None, target=None, i_sprite = None, f_sprite = None):
        self.weight = weight
        self.volume = volume
        self.use_function = use_function
        self.value = value
        self.name = name
        self.target = target
        self.i_sprite = i_sprite
        self.f_sprite = f_sprite

    ## TODO pick up stuffs
    def pick_up(self, actor):
        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room")
            else:
                # game_message(f'{self.name} Picked up')
                # actor.container.inventory.append(self.owner)
                # GAME.current_objects.remove(self.owner)
                # self.container = actor.container
                game_message(f'{self.name} Picked up')
                actor.container.inventory.append(self.owner)
                for x in PLAYER.container.inventory:
                    constants.Player_array = [1 if 0 else 0 for x in PLAYER.container.inventory]
                    # constants.Player_array[x] = "1"
                GAME.current_objects.remove(self.owner)
                self.container = actor.container

    ## TODO drop item

    def drop_down(self, new_x, new_y):

        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)

        self.owner.x = new_x
        self.owner.y = new_y

        game_message(self.owner.item.name + " dropped")

    # def item_examine(self):
    #     game_message("This is a " + self.name)
    #     return self.name
    #
    # def equip(self, actor):
    #     game_message("You've equipped " + self.name)
    #     actor.creature.gear.power = self.value
    #     actor.creature.gear.i_sprite = self.i_sprite
    #     self.container.inventory.remove(self.owner)
    # def equip(self, actor):
    #     game_message("You've equipped " + self.name)
    #     actor.creature.gear.att = self.value
    #     ASSETS.Sword = self.i_sprite
    #     self.container.inventory.remove(self.owner)

    ## TODO use item
    # def use(self):
    #     if self.use_function:
    #         result = self.use_function(self.value,self.owner)
    #         if result is not None:
    #             print("use function failed")
    #         else:
    #             self.container.inventory.remove(self.owner)
    def use(self):
        if self.use_function:
            result = self.use_function(self.value,self.container.owner)
            if result is not None:
                print("use function failed")
            else:
                self.container.inventory.remove(self.owner)


##########################################

###             MAGIC                  ###

##########################################
class com_Magic:
    def __init__(self, name,target,value):
        self.name = name
        self.target = target
        self.value = value


def spell_list(spell):
    spells ={'ThunderSpell': 7, 'HealWand':5}
    #thunder = com_Magic("ThunderBoom", "target", 50)

    return (spells.get(spell))


def cast_heal(value,target):

    if target.creature.hp == target.creature.maxhp:
        game_message(target.name_object + " already at max hp! ", constants.COLOR_GREEN)

        return "canceled"
    else:
        game_message(f'{target.creature.name_instance} healed for {str(value)}', constants.COLOR_GREEN)
        target.creature.heal(value)


def cast_thunder(value,caster):
    if caster.creature.spellcast(value)=="canceled":
        game_message("Target not found",constants.COLOR_GREEN)
        return "canceled"



###############################################################

###                          MOUSE                          ###

###############################################################


def mouse_click(click_x, click_y, button):
    #print (button)
    click_tup = (click_x, click_y)
    global FOV_CALCULATE
    click_on_item = (constants.Item_L_self_x - 10 <= click_x <= constants.Item_L_self_x + 210
            and constants.Item_L_self_y - 20 <= click_y <= constants.Item_L_self_y + 65)
    click_on_item_ahead = (constants.Item_ahead_x - 10 <= click_x <= constants.Item_ahead_x + 210
            and constants.Item_ahead_y - 20 <= click_y <= constants.Item_ahead_y + 65)
    target = map_check_for_creatures(PLAYER.x + constants.P_controls_x[PLAYER.facing],
                                     PLAYER.y + constants.P_controls_y[PLAYER.facing],
                                     PLAYER)
    # target_item = map_check_for_items(PLAYER.x,PLAYER.y)
    objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)
    objects_infront_player = map_objects_at_coords(PLAYER.x+constants.P_controls_x[PLAYER.facing],PLAYER.y+constants.P_controls_y[PLAYER.facing])
    click_on_alcove = (250 <= click_x <= 550
            and 250 <= click_y <= 350)
    ## Item on ground
    if click_on_item:
        if objects_at_player:
            for obj in reversed(objects_at_player):
                if button == 1:
                    if len(MOUSE) == 0:
                        obj.mouse_pick_up(MOUSE)
                    else:
                        MOUSE[-1].mouse_drop(PLAYER.x, PLAYER.y)
                if button == 3:

                    game_message(f'Examine: {obj.name}', constants.COLOR_YELLOW)

                return "actioned"

        elif len(MOUSE) == 1 and button == 1:

            MOUSE[-1].mouse_drop(PLAYER.x, PLAYER.y)

            return "actioned"
    if click_on_item_ahead and not GAME.current_map[PLAYER.x+constants.P_controls_x[PLAYER.facing]][PLAYER.y+constants.P_controls_y[PLAYER.facing]].block_path:

        if objects_infront_player:
            for obj in reversed(objects_infront_player):
                if button == 1:
                    if len(MOUSE) == 0:
                        obj.mouse_pick_up(MOUSE)
                        return "actioned"
                    else:
                        MOUSE[-1].mouse_drop(PLAYER.x + constants.P_controls_x[PLAYER.facing],
                                 PLAYER.y + constants.P_controls_y[PLAYER.facing])

                        return "actioned"
        elif len(MOUSE) == 1:

            MOUSE[-1].mouse_drop(PLAYER.x + constants.P_controls_x[PLAYER.facing],
                                 PLAYER.y + constants.P_controls_y[PLAYER.facing])

            return "actioned"

    if click_on_alcove and (GAME.current_map[PLAYER.x+constants.P_controls_x[PLAYER.facing]][PLAYER.y+constants.P_controls_y[PLAYER.facing]].wall_alcove):

        if objects_infront_player:
            for obj in reversed(objects_infront_player):
                if button == 1:
                    if len(MOUSE) == 0:
                        obj.mouse_pick_up(MOUSE)
                        return "actioned"
                    else:
                        MOUSE[-1].mouse_drop(PLAYER.x + constants.P_controls_x[PLAYER.facing],
                                 PLAYER.y + constants.P_controls_y[PLAYER.facing])
                        return "actioned"
        elif len(MOUSE) == 1:

            MOUSE[-1].mouse_drop(PLAYER.x + constants.P_controls_x[PLAYER.facing],
                                 PLAYER.y + constants.P_controls_y[PLAYER.facing])
        # if len(MOUSE) != 0:
        #
        # else:
        #     print(f'{objects_infront_player}')
        return "actioned"
    ## Bottom Inventory
    for n in range(0, 8):
        if (n * 50 + 20) <= click_x < (n * 50 + 60) and n < len(PLAYER.container.inventory) and 662 < click_y < 702:
            if button == 3:
                PLAYER.container.inventory[n].item_examine(n+1)

            elif button == 1:
                #print(PLAYER.creature.gear)
                PLAYER.container.inventory[n].drop_down(PLAYER.x, PLAYER.y)

                #PLAYER.container.inventory[n].equip(PLAYER,n-1)
                # PLAYER.container.inventory.remove(PLAYER.container.inventory[n-1])
            return "actioned"
        elif ((n * 50 + 20) <= click_x < (n * 50 + 60) and 662 < click_y < 702) and n >= len(PLAYER.container.inventory):
            game_message(f'No item in slot {n+1}')

    #
    # for n in range(0, len(PLAYER.container.inventory)):
    #     if (n * 50 + 20) <= click_x < (n * 50 + 60):
    #         if button == 3:
    #             PLAYER.container.inventory[n].item_examine()
    #
    #
    #         elif button == 1:
    #             # print(PLAYER.creature.gear)
    #             PLAYER.container.inventory[n].drop_down(PLAYER.x, PLAYER.y)
    #
    #             # PLAYER.container.inventory[n].equip(PLAYER,n-1)
    #             # PLAYER.container.inventory.remove(PLAYER.container.inventory[n-1])
    #         return "actioned"

    ## Hero Face
    if ((ASSETS.hero_face <= click_x < ASSETS.hero_face + constants.IMG_Portrait1.get_width()) and
    ASSETS.right_ui_posy <= click_y < ASSETS.right_ui_posy + constants.IMG_Portrait1.get_height()):

        if len(MOUSE) == 0:
            print("tried to equip, nothing to equip")
        else:

            MOUSE[0].equip(PLAYER, MOUSE[0])
            MOUSE.remove(MOUSE[0])

        return "actioned"


    ## SpellBook
    if ((ASSETS.right_ui_posx + 10 <= click_x <= ASSETS.right_ui_posx + 10 + ASSETS.SpellBook.get_width())
        and (ASSETS.right_ui_posy + 50 <= click_y <= ASSETS.right_ui_posy + 50 + ASSETS.SpellBook.get_height())):
        game_message("SpellBook opened", constants.COLOR_GREEN)
        draw_game()
        spellbook()

        return "actioned"

    if (((ASSETS.right_ui_posx + 10 <= click_x <= ASSETS.right_ui_posx + 10 + ASSETS.Sword.get_width())
            and (ASSETS.right_ui_posy + ASSETS.SpellBook.get_height() + 50 <= click_y <=
                 (ASSETS.right_ui_posy + ASSETS.SpellBook.get_height() + ASSETS.Sword.get_height() + 50)))):

        if button == 1:
            mon_check(PLAYER.creature.atack(tcod.random_get_int(0, 1, PLAYER.creature.gear.power)))

        elif button == 3:
            if PLAYER.creature.gear.name != "Fist" and len(MOUSE) == 0 :
                PLAYER.creature.gear.unequip(PLAYER.x, PLAYER.y)
            elif PLAYER.creature.gear.name == "Fist" and len(MOUSE) ==0:
                game_message("That's a hand for slapping monsters!")
            elif PLAYER.creature.gear.name == "Fist" and len(MOUSE) != 0 :
                MOUSE[0].equip(PLAYER, MOUSE[0])
                MOUSE.remove(MOUSE[0])
            else: ## Replaces held item with equipped item
                PLAYER.creature.gear.replace(PLAYER.creature.gear, MOUSE[0])

        return "actioned"


    ## Buttons
    if target:

        if target.creature.type == "Door":
        ## DOOR
            if ((constants.D_button_x[0] <= click_x < constants.D_button_x[1]) and
                (constants.D_button_y[0] <= click_y < constants.D_button_y[1])
                and target.creature.type == "Door" and (target.status == "Closed" or target.status =="Locked")) or \
                    ((615 <= click_x < 655) and (320 <= click_y < 400)
                     and target.creature.type == "Door" and target.status == "Open"):
                if target.status != "Locked":
                    if target.status == "Closed":
                        print(target.creature.name_instance)
                        door_helper(target,target.creature.type)
                    elif target.status == "Open":
                        door_helper(target,target.creature.type)
                elif len(MOUSE)== 1:
                    if MOUSE[0].check_item(target.item):
                        door_helper(target,target.creature.type)

                else:
                    game_message(f'Door is locked!', constants.COLOR_RED)
                map_make_fov(GAME.current_map)
                FOV_CALCULATE = True

        ## Wall Button
        elif target.creature.type == "Button" and (
                (constants.W_button_x <= click_x < constants.W_button_x + constants.wall_button_bc.get_width()) and
                (constants.W_button_y <= click_y < constants.W_button_y + constants.wall_button_bc.get_height())):
            #if target.creature.name_instance == target.target_obj:
            if target.target_obj and target.status == "Closed":

                door_helper(target.target_obj, target.creature.type)
                target.status = "Used"
                target.crawl_sprite = target.sprite_anim[1]
            elif target.target_obj and target.status == "Used":
                game_message(f'Already used',constants.COLOR_YELLOW)
            else:
                print("something went wrong")
            map_make_fov(GAME.current_map)
            FOV_CALCULATE = True

        return "actioned"

    else:
        game_message("Mouse clicked, no action", constants.COLOR_GREEN)

###############################################################

###                          MAP                            ###

###############################################################


def map_create():
    L1_map = constants.Map_BC_L1
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)]
               for x in range(0, constants.MAP_WIDTH)]  # goes through whole program area
    img_w, img_h = L1_map.size
    # img_w, img_h = L1_map.size
    # print (img_w,img_h)
    if constants.MAP_HEIGHT < img_h:
        img_h = img_h - (img_h - constants.MAP_HEIGHT)
    if constants.MAP_WIDTH < img_w:
        img_w = img_w - (img_w - constants.MAP_WIDTH)

    for y in range(0, img_h): #img_h == 16
        for x in range(0, img_w): #img_w == 16
            if L1_map.getpixel((x,y)) == (0,0,0):
                new_map[x][y].block_path = True
            if L1_map.getpixel((x,y)) == (180,180,180): ## Removable walls
                new_map[x][y].block_path = True
            if L1_map.getpixel((x,y)) == (0,255,0):
                new_map[x][y].door_path = True

    map_make_fov(new_map)

    return new_map

def heck_for_items(x,y,excluded = None):
    target = None
        # check object list to find creature at that location which is excluded
    for obj in GAME.interact_objects:

        if (obj.x == x and
                obj.y == y):
                #obj.creature):
            target = obj

        if target:
            return target

# def map_check_for_items(x,y,exclude_object = None):
#     item_target = None
#     for game_obj in GAME.current_objects:
#         if not game_obj == PLAYER and not game_obj.creature and game_obj.x == x and game_obj.y == y:
#             item_target = game_obj
#         elif item_target:
#             return item_target



def checker(x,y,excluded = None):
    target = None
    item = None
        # check object list to find creature at that location which is excluded
    for obj in GAME.interact_objects:

        if (obj.x == x and
                obj.y == y):
                #obj.creature):
            item = obj

        # if item:
        #     return item
    if excluded:
        # check object list to find creature at that location which is excluded
        for obj in GAME.current_objects:

            if (obj is not excluded and
                    obj.x == x and
                    obj.y == y and
                    obj.creature):
                    #obj.creature):
                target = obj
            #
            # if target:
    return target,item

def map_check_for_creatures(x, y, exclude_object = None):
    target = None

    if exclude_object:
        # check object list to find creature at that location which is excluded
        for obj in GAME.current_objects:

            if (obj is not exclude_object and
                    obj.x == x and
                    obj.y == y and
                    obj.creature):
                    #obj.creature):
                target = obj

            if target:
                return target

        # for obj in GAME.interact_objects:
        #
        #     if (obj.x == x and
        #             obj.y == y):
        #         # obj.creature):
        #         target2 = obj
        #
        #     if target2:
        #         return target2
    else:
        print("no targetr")
        # check object list to find creature at that location which is excluded
        for obj in GAME.current_objects:
            if object.x == x and obj.y == y and obj.creature:
                target = obj

            if target:
                return target




def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = tcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    # deprecationWarning fixed with FOV_MAP = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    # If any new FOV blocks will be created, make sure to add them here for appropriate fov calculation
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            tcod.map_set_properties(FOV_MAP, x, y,
                                    not incoming_map[x][y].block_path and not incoming_map[x][y].door_path,
                                    not incoming_map[x][y].block_path and not incoming_map[x][y].door_path)


def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        tcod.map_compute_fov(FOV_MAP,PLAYER.x,PLAYER.y,constants.TORCH_RADIUS,
                             constants.FOV_LIGHT_WALLS,constants.FOV_ALGO)

def map_objects_at_coords(coords_x, coords_y):
    object_options = [obj for obj in GAME.interact_objects
                      if obj.x == coords_x and obj.y == coords_y and not obj == PLAYER]
    return object_options
###################################################

###                   DRAWING                   ###

###################################################

def draw_game():

    # surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # map
    draw_fpp()
    draw_UI()

    # ###  draw Characters
    draw_debug()
    draw_messages()

    if len(MOUSE) ==1:
        MouseX, MouseY = (pygame.mouse.get_pos())
        SURFACE_MAIN.blit(MOUSE[len(PLAYER.container.inventory) - 1].f_sprite,
                          (MouseX - 50, MouseY - 10))

    # pygame.gfxdraw.textured_polygon(SURFACE_MAIN,((100,200),(800,800),(300,400),(200,500)),constants.S_BEHO_LOL,100,100)

    # tryhard = pygame.gfxdraw.textured_polygon(SURFACE_MAIN,((0,100),(400,200),(400,300),(100,500)),constants.door1_mid,100,100)
    # tryhard.blit(constants.S_BEHO_LOL,(0,0))
    # SURFACE_MAIN.blit(constants.S_BEHO_LOL,(100,100))
    # update display
    pygame.display.flip()


#TODO drawing doesnt work, why?

def mon_check(action):
    for game_obj in GAME.current_objects:
        # if ((PLAYER.x - constants.L_controls_x[PLAYER.facing] == game_obj.x)
        #         and (PLAYER.y - constants.L_controls_y[PLAYER.facing] == game_obj.y)):
        #     if action == "draw":
        #         if game_obj.creature and game_obj.creature.object_type == "Monster":
        #             print (game_obj.creature.object_type)
        #             SURFACE_MAIN.blit(game_obj.crawl_sprite, (constants.M_mid_monster))
        #         elif game_obj.creature and game_obj.creature.object_type == "Wall":
        #
        #             SURFACE_MAIN.blit(game_obj.crawl_sprite, (constants.M_mid_wall))
        #         else:
        #             SURFACE_MAIN.blit(game_obj.crawl_sprite, (140,500))
        #     else:
        #         return True
        if ((PLAYER.x - constants.L_controls_x[PLAYER.facing] -1 == game_obj.x)
                and (PLAYER.y - constants.L_controls_y[PLAYER.facing] == game_obj.y)):
            if action == "draw":
                print("yup tehre's somthin") # SURFACE_MAIN.blit(game_obj.item.i_sprite, (140, 500))
        else:
            False


# def draw_monster(x, y): #TODO sprawdz to
#     for game_obj in GAME.current_objects:
#         if (PLAYER.x - x == game_obj.x ) and (PLAYER.y -y == game_obj.y):
#            # target = ((PLAYER.x - x == game_obj.x ) and (PLAYER.y -y == game_obj.y))
#             SURFACE_MAIN.blit(game_obj.crawl_sprite, (400,300))


def draw_map(map_to_draw):

    top_right_map = (constants.GAME_WIDTH - 256)
    # top_right_map = (32)
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            is_visible = tcod.map_is_in_fov(FOV_MAP, x, y)
            if is_visible:
                map_to_draw[x][y].explored = True

    map_size = (len(constants.UI_Minimap_dist)+2)*16
    # pygame.draw.rect(SURFACE_MAIN, constants.COLOR_GRAY,(1120,16,map_size,map_size))

    top_left = 0
    # for x in  abc:
    #     for y in abc:
    for x in range(-3,4):
        for y in range(-3,4):

            ###
            if map_to_draw[PLAYER.x + x][PLAYER.y + y].explored:
                if map_to_draw[PLAYER.x + x][PLAYER.y + y].block_path:
                    # Draw Wall
                    SURFACE_MAIN.blit(constants.S_WALL,
                                      (constants.MINI_x + ((constants.UI_Minimap_dist.index(x) + 1) * constants.CELL_WIDTH),
                                       constants.MINI_y + ((constants.UI_Minimap_dist.index(y) + 1) * constants.CELL_HEIGHT)))
                elif map_to_draw[PLAYER.x + x][
                    PLAYER.y + y].block_path == False and x < top_right_map + constants.CELL_WIDTH and y < constants.CELL_HEIGHT:
                    # Draw floor
                    SURFACE_MAIN.blit(constants.S_FLOOR, ( constants.MINI_x + ((constants.UI_Minimap_dist.index(x) + 1) * constants.CELL_WIDTH),
                                                         constants.MINI_y + ((constants.UI_Minimap_dist.index(y) + 1) * constants.CELL_HEIGHT)))
            # elif not map_to_draw[PLAYER.x + x][PLAYER.y + y].explored:
            #     pygame.draw.rect(SURFACE_MAIN, constants.COLOR_BLACK, (
            #     (constants.UI_Minimap_dist.index(x) + 1) * 16, (constants.UI_Minimap_dist.index(y) + 1) * 16, 16, 16))

    for obj in GAME.current_objects:
        obj.draw()

        if obj == obj_Actor:
            print("YUP")
    # SURFACE_MAIN.blit(constants.ramka,(0,0))
    SURFACE_MAIN.blit(constants.ramka, constants.MINI_map)


def draw_debug():
    clock = "FPS:" + str(int(CLOCK.get_fps()))
    p_hp = "HP:" + str(PLAYER.creature.hp) + "/" + str(PLAYER.creature.maxhp)
    power = "STR:" + str(PLAYER.creature.gear.power)
    text_to_draw = [clock, p_hp, power]
    pos_y = 0
    for text in text_to_draw:
        draw_left(SURFACE_MAIN, text, (constants.GAME_WIDTH-470,pos_y+20), constants.COLOR_GREEN)
        pos_y += 15


def draw_map_items(map_item_name):

    draw_left(SURFACE_MAIN, "Object: " + map_item_name, (40,20), constants.COLOR_GREEN)


def draw_messages():

    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

    start_y = constants.GAME_HEIGHT - (constants.NUM_MESSAGES * text_height)
    start_x = 5 - (constants.NUM_MESSAGES * text_height)
    i = 0
    for message, color in to_draw:
        draw_BL(SURFACE_MAIN, message,(807, start_y + (i * text_height)-280) , color,constants.COLOR_BLACK)
        i += 1


def draw_text(display_surface, text_to_display, T_text_coords, text_color, back_color=None):

    # text_x, text_y = T_text_coords
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    text_rect.topright = T_text_coords
    display_surface.blit(text_surf, text_rect)


def draw_center(display_surface, text_to_display, T_text_coords, text_color, back_color=None):

    # text_x, text_y = T_text_coords
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    text_rect.topleft = T_text_coords
    display_surface.blit(text_surf, text_rect)


def draw_left(display_surface, text_to_display, T_text_coords, text_color, back_color=constants.COLOR_BLACK):

    # text_x, text_y = T_text_coords
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    text_rect.topleft = T_text_coords
    display_surface.blit(text_surf, text_rect)


def draw_BL(display_surface, text_to_display, T_text_coords, text_color, back_color=None):

    # text_x, text_y = T_text_coords
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    text_rect.bottomleft = T_text_coords
    display_surface.blit(text_surf, text_rect)

def check_target(target,distance):
    if target:
        if target.creature.object_type == "Monster" or target.creature.object_type == "Container":
            target.crawl_sprite = target.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
            if distance==0:
                SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y[distance])
            elif distance >0 and distance <4:
                # SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y[distance])
                SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite,
                                                          (int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Scaler[distance])))),
                                  constants.monsterX_Y[distance])

        if target.creature.object_type == "Button" and target.facing == PLAYER.facing:
            SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Scaler[distance])))), constants.buttonX_Y[distance])
        elif target.creature.object_type == "Door":
            SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Door_scaler[distance])))), constants.doorX_Y[distance])

        elif target.creature.object_type == "Alcove" :
            SURFACE_MAIN.blit(pygame.transform.scale(target.crawl_sprite,
                              (int(constants.alcove.get_width() * constants.Scaler[distance]),
                               int(constants.alcove.get_height() * constants.Scaler[distance]))),
                              constants.alcoveCenter[distance+1])
            # check_item(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 1, PLAYER.x, PLAYER.y - 1)

def check_target_R(target,distance):
    if target:
        if target.creature.object_type == "Monster" or target.creature.object_type == "Container":
            target.crawl_sprite = target.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
            if distance==0:
                SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y2[distance])
            elif distance >0 and distance <4:
                # SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y[distance])
                SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite,
                                                          (int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Scaler[distance])))),
                                  constants.monsterX_Y2[distance])

        if target.creature.object_type == "Button":
            if target.facing == PLAYER.facing:
                SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (
                int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                int(target.crawl_sprite.get_height() * constants.Scaler[distance])))), constants.buttonX_Y2[distance])
            elif PLAYER.facing != target.facing and (target.facing + PLAYER.facing) %2 != PLAYER.facing %2:
                SURFACE_MAIN.blit(
                   (pygame.transform.scale( pygame.transform.flip(constants.wall_button_L,True,False), (
                int(constants.wall_button_L.get_width() * constants.Scaler[distance]),
                int(constants.wall_button_L.get_height() * constants.Scaler[distance])))), constants.buttonX_Y2[distance])

        elif target.creature.object_type == "Door":
            SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (int(target.crawl_sprite.get_width() * constants.Door_scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Door_scaler[distance])))), constants.doorX_Y2[distance])


def check_item(target,distance,xdist,ydist = None):
    if target:
        for obj in GAME.interact_objects:
            if xdist == obj.x and ydist == obj.y:
                if GAME.current_map[obj.x][obj.y].wall_alcove:
                    SURFACE_MAIN.blit((pygame.transform.scale(obj.f_sprite,
                                                              (
                                                                  int(obj.f_sprite.get_width() * constants.itemScaler[
                                                                      distance]),
                                                                  int(obj.f_sprite.get_height() * constants.itemScaler[
                                                                      distance])))),constants.itemX_Y_Alc[distance])
                    print("ALCOVE")
                else:
                    SURFACE_MAIN.blit((pygame.transform.scale(obj.f_sprite,
                                                              (
                                                                  int(obj.f_sprite.get_width() * constants.itemScaler[
                                                                      distance]),
                                                                  int(obj.f_sprite.get_height() * constants.itemScaler[
                                                                      distance])))),constants.itemX_Y[distance])
def check_item_R(target,distance,xdist,ydist):

    if target:
        for obj in GAME.interact_objects:
            if xdist == obj.x and ydist == obj.y:
                SURFACE_MAIN.blit((pygame.transform.scale(obj.f_sprite,
                                                      (
                                                      int(obj.f_sprite.get_width() * constants.itemScaler[distance]),
                                                      int(obj.f_sprite.get_height() * constants.itemScaler[
                                                          distance])))),
                              constants.itemX_Y_R[distance])


def check_item_L(target,distance,xdist,ydist):

    if target:
        for obj in GAME.interact_objects:
            if xdist == obj.x and ydist == obj.y:
                SURFACE_MAIN.blit((pygame.transform.scale(obj.f_sprite,
                                                      (
                                                      int(obj.f_sprite.get_width() * constants.itemScaler[distance]),
                                                      int(obj.f_sprite.get_height() * constants.itemScaler[
                                                          distance])))),
                              constants.itemX_Y_L[distance])


def check_target_L(target,distance):
    if target:
        if target.creature.object_type == "Monster" or target.creature.object_type == "Container":
            target.crawl_sprite = target.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
            if distance==0:
                SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y1[distance])
            elif distance >0 and distance <4:
                # SURFACE_MAIN.blit(target.crawl_sprite, constants.monsterX_Y[distance])
                SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite,
                                                          (int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Scaler[distance])))),
                                  constants.monsterX_Y1[distance])

        # if target.creature.object_type == "Button":
        #     if target.facing == constants.L_facing[PLAYER.facing]:
        #         SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (
        #         int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
        #         int(target.crawl_sprite.get_height() * constants.Scaler[distance])))), constants.buttonX_Y1[distance])
        if target.creature.object_type == "Button":
            if target.facing == PLAYER.facing:
                SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (
                int(target.crawl_sprite.get_width() * constants.Scaler[distance]),
                int(target.crawl_sprite.get_height() * constants.Scaler[distance])))), constants.buttonX_Y1[distance])
            elif PLAYER.facing != target.facing and (target.facing + PLAYER.facing) %2 != PLAYER.facing %2:
                SURFACE_MAIN.blit((pygame.transform.scale(pygame.transform.flip(constants.wall_button_L,False,False), (
                int(constants.wall_button_L.get_width() * constants.Scaler[distance]),
                int(constants.wall_button_L.get_height() * constants.Scaler[distance])))), constants.side_buttonX_Y1[distance])

        elif target.creature.object_type == "Door":
            SURFACE_MAIN.blit((pygame.transform.scale(target.crawl_sprite, (int(target.crawl_sprite.get_width() * constants.Door_scaler[distance]),
                                                           int(target.crawl_sprite.get_height() * constants.Door_scaler[distance])))), constants.doorX_Y1[distance])

# def draw_helper_objects(target1,target2,target3):
#     # if target3 and target3.creature.object_type == "Monster":
#
#
#     if target3:
#         ts3w = int(target3.crawl_sprite.get_width() * 0.3)
#         ts3h = int(target3.crawl_sprite.get_height() * 0.3)
#         if target3.creature.object_type == "Monster":
#             target3.crawl_sprite = target3.sprite_anim_far[int((pygame.time.get_ticks() / 500) % 2)]
#             SURFACE_MAIN.blit((pygame.transform.scale(target3.crawl_sprite, (ts3w, ts3h))), constants.monsterX_Y[2])
#         elif target3.creature.object_type == "Button":
#             SURFACE_MAIN.blit((pygame.transform.scale(target3.crawl_sprite, (ts3w, ts3h))), constants.buttonX_Y[2])
#         else:
#             SURFACE_MAIN.blit((pygame.transform.scale(target3.crawl_sprite, (ts3w, ts3h))), constants.doorX_Y[2])
#
#     if target2:
#         ts2w = int(target2.crawl_sprite.get_width() * 0.6)
#         ts2h = int(target2.crawl_sprite.get_height() * 0.6)
#
#         if target2.creature.object_type == "Monster":
#             target2.crawl_sprite = target2.sprite_anim_far[int((pygame.time.get_ticks() / 500) % 2)]
#             SURFACE_MAIN.blit((pygame.transform.scale(target2.crawl_sprite, (ts2w, ts2h))), constants.monsterX_Y[1])
#
#         elif target2.creature.object_type == "Button":
#             SURFACE_MAIN.blit((pygame.transform.scale(target2.crawl_sprite, (ts2w, ts2h))), constants.buttonX_Y[1])
#
#         else:
#             SURFACE_MAIN.blit((pygame.transform.scale(target2.crawl_sprite, (ts2w, ts2h))), constants.doorX_Y[1])
#
#     if target1:
#         if target1.creature.object_type == "Monster":
#             target1.crawl_sprite = target1.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
#             SURFACE_MAIN.blit(target1.crawl_sprite, constants.monsterX_Y[0])
#         elif target1.creature.object_type == "Button":
#             SURFACE_MAIN.blit(target1.crawl_sprite, constants.buttonX_Y[0])
#         else:
#             SURFACE_MAIN.blit(target1.crawl_sprite, constants.doorX_Y[0])

        #


# def draw_objects():
#
#     #
#     # if PLAYER.facing == 0:
#     #     draw_helper_objects(map_check_for_creatures(PLAYER.x, PLAYER.y - 1, PLAYER),
#     #                     map_check_for_creatures(PLAYER.x, PLAYER.y - 2, PLAYER),
#     #                     map_check_for_creatures(PLAYER.x, PLAYER.y - 3, PLAYER))
#
#
#     if PLAYER.facing == 1:
#         draw_helper_objects(map_check_for_creatures(PLAYER.x + 1,PLAYER.y,PLAYER),
#                             map_check_for_creatures(PLAYER.x + 2,PLAYER.y,PLAYER),
#                             map_check_for_creatures(PLAYER.x + 3,PLAYER.y,PLAYER))
#
#
#     elif PLAYER.facing == 2:
#         draw_helper_objects(map_check_for_creatures(PLAYER.x, PLAYER.y + 1, PLAYER),
#                             map_check_for_creatures(PLAYER.x, PLAYER.y + 2, PLAYER),
#                             map_check_for_creatures(PLAYER.x, PLAYER.y + 3, PLAYER))
#
#
#     elif PLAYER.facing == 3:
#         draw_helper_objects(map_check_for_creatures(PLAYER.x - 1,PLAYER.y,PLAYER),
#                             map_check_for_creatures(PLAYER.x - 2,PLAYER.y,PLAYER),
#                             map_check_for_creatures(PLAYER.x - 3,PLAYER.y,PLAYER))
#
#     for game_obj in GAME.current_objects:
#         if not game_obj == PLAYER:
#             if not game_obj.creature and PLAYER.x == game_obj.x and PLAYER.y == game_obj.y:
#                 SURFACE_MAIN.blit(game_obj.item.f_sprite, constants.Item_L_self)


def draw_items(x, y):
    for game_obj in GAME.current_objects:
        if not game_obj == PLAYER:
            if not game_obj.creature and PLAYER.x == game_obj.x and PLAYER.y == game_obj.y:
                SURFACE_MAIN.blit(game_obj.item.f_sprite, constants.Item_L_self)

def draw_fpp():
    # TODO add left/right -2/+2 wall draws
    # draw FLOOR !@#$!@#%
    SURFACE_MAIN.blit(constants.G_Floor[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)], (16,400))
    SURFACE_MAIN.blit(constants.G_Ceiling[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)], (16,16))


    if PLAYER.facing == 0:  # "N":

        if GAME.current_map[PLAYER.x-1][PLAYER.y -3].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][0],
                                    (constants.L_Walls_Pos[0]))
        if check_target_L(map_check_for_creatures(PLAYER.x-1, PLAYER.y - 3, PLAYER), 2):
            pass
        if check_item_L(heck_for_items(PLAYER.x-1, PLAYER.y - 3, PLAYER), 3,PLAYER.x-1, PLAYER.y - 3):
            pass
        # if check_target_L

        if GAME.current_map[PLAYER.x-1][PLAYER.y -2].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                                    (constants.L_Walls_Pos[1]))
        if check_target_L(map_check_for_creatures(PLAYER.x - 1, PLAYER.y - 2, PLAYER), 1):
            pass
        if check_item_L(heck_for_items(PLAYER.x-1, PLAYER.y - 2, PLAYER), 2,PLAYER.x-1, PLAYER.y - 2):
            pass

        if GAME.current_map[PLAYER.x-1][PLAYER.y -1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                                    (constants.L_Walls_Pos[2]))
        if check_target_L(map_check_for_creatures(PLAYER.x - 1, PLAYER.y - 1, PLAYER), 0):
            pass
        if check_item_L(heck_for_items(PLAYER.x-1, PLAYER.y - 1, PLAYER), 1,PLAYER.x-1, PLAYER.y - 1):
            pass

        if GAME.current_map[PLAYER.x-1][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                                    (constants.L_Walls_Pos[3]))

        if check_item_L(heck_for_items(PLAYER.x-1, PLAYER.y, PLAYER), 0, PLAYER.x-1, PLAYER.y):
            pass



        if GAME.current_map[PLAYER.x+1][PLAYER.y-3].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][0],
                              (constants.R_Walls_Pos[0]))
        if check_target_R(map_check_for_creatures(PLAYER.x+1, PLAYER.y - 3, PLAYER), 2):
            pass
        if check_item_R(heck_for_items(PLAYER.x+1, PLAYER.y - 3, PLAYER), 3,PLAYER.x+1, PLAYER.y - 3):
            pass


        if GAME.current_map[PLAYER.x+1][PLAYER.y-2].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                              (constants.R_Walls_Pos[1]))
        if check_target_R(map_check_for_creatures(PLAYER.x+1, PLAYER.y - 2, PLAYER), 1):
            pass
        if check_item_R(heck_for_items(PLAYER.x+1, PLAYER.y - 2, PLAYER), 2,PLAYER.x+1, PLAYER.y - 2):
            pass


        if GAME.current_map[PLAYER.x+1][PLAYER.y-1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                              (constants.R_Walls_Pos[2]))
        if check_target_R(map_check_for_creatures(PLAYER.x+1, PLAYER.y - 1, PLAYER), 0):
            pass
        if check_item_R(heck_for_items(PLAYER.x+1, PLAYER.y - 1, PLAYER), 1,PLAYER.x+1, PLAYER.y - 1):
            pass


        if GAME.current_map[PLAYER.x+1][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                              (constants.R_Walls_Pos[3]))



        if check_item_R(heck_for_items(PLAYER.x+1, PLAYER.y, PLAYER), 0,PLAYER.x+1, PLAYER.y):
            pass

        ## Center:


        if GAME.current_map[PLAYER.x][PLAYER.y - 3].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][0],
                              (constants.M_Walls_Pos[0]))

        if GAME.current_map[PLAYER.x][PLAYER.y - 3].wall_alcove:
            # SURFACE_MAIN.blit(pygame.transform.scale(constants.alcove,
            #                   (int(constants.alcove.get_width() * constants.Scaler[2]),
            #                    int(constants.alcove.get_height() * constants.Scaler[2]))),
            #                   constants.alcoveCenter[3])
                SURFACE_MAIN.blit(constants.alcoves[2], constants.alcoveCenter[3])
        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y - 3, PLAYER),2):
            pass
        if check_item(heck_for_items(PLAYER.x, PLAYER.y - 3, PLAYER), 3,PLAYER.x, PLAYER.y -3):
            pass

        if GAME.current_map[PLAYER.x][PLAYER.y - 2].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                              (constants.M_Walls_Pos[1]))

            if GAME.current_map[PLAYER.x][PLAYER.y - 2].wall_alcove:
                SURFACE_MAIN.blit(constants.alcoves[1], constants.alcoveCenter[2])
        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y - 2, PLAYER),1):
            pass
        if check_item(heck_for_items(PLAYER.x, PLAYER.y - 2, PLAYER), 2,PLAYER.x,PLAYER.y -2):
            pass


        if GAME.current_map[PLAYER.x][PLAYER.y - 1].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                              (constants.M_Walls_Pos[2]))
        # if GAME.current_map[PLAYER.x][PLAYER.y - 1].wall_alcove:
        #     SURFACE_MAIN.blit(constants.alcove, constants.alcoveCenter[1])
        if check_item(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 1, PLAYER.x, PLAYER.y-1):
            pass

        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y - 1, PLAYER),0):
            pass

        # if check_item(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 1, PLAYER.x, PLAYER.y-1):
        #     pass


        if GAME.current_map[PLAYER.x][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                              (constants.M_Walls_Pos[3]))





    if PLAYER.facing == 1:

        #leftie
        # for side in constants.random_range:

        for distance, walls in zip(range(3,-1,-1),range(0,4,1)):
            if GAME.current_map[PLAYER.x+distance][PLAYER.y-1].block_path:
                SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][walls],
                                  (constants.L_Walls_Pos[walls]))
            if map_check_for_creatures(PLAYER.x + distance, PLAYER.y-1, PLAYER):
                for obj in GAME.current_objects:
                    obj.draw_self_fpp(distance)

            check_item_L(heck_for_items(PLAYER.x+distance, PLAYER.y-1, PLAYER), distance,PLAYER.x+distance, PLAYER.y-1)

        # if check_item_L(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 0,PLAYER.x, PLAYER.y - 1):
        #     pass


        ## IRGHTIE

        for distance, walls in zip(range(3,-1,-1),range(0,4,1)):
            if GAME.current_map[PLAYER.x+distance][PLAYER.y+1].block_path:
                SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][walls],
                                  (constants.R_Walls_Pos[walls]))
            if map_check_for_creatures(PLAYER.x + distance, PLAYER.y+1, PLAYER):
                for obj in GAME.current_objects:
                    obj.draw_self_fpp(distance)

            check_item_R(heck_for_items(PLAYER.x+distance, PLAYER.y+1, PLAYER), distance,PLAYER.x+distance, PLAYER.y+1)
        # if check_item_R(heck_for_items(PLAYER.x, PLAYER.y + 1, PLAYER), 0,PLAYER.x, PLAYER.y + 1):
        #     pass


        # #centerie
        for distance, walls in zip(range(3,-1,-1),range(0,4,1)):
            if GAME.current_map[PLAYER.x+distance][PLAYER.y].block_path:
                SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][walls],
                                  (constants.M_Walls_Pos[walls]))
            if map_check_for_creatures(PLAYER.x + distance, PLAYER.y, PLAYER):
                for obj in GAME.current_objects:
                    obj.draw_self_fpp(distance)

            check_item(heck_for_items(PLAYER.x+distance, PLAYER.y, PLAYER), distance,PLAYER.x+distance, PLAYER.y)


    #
    #
    #         if GAME.current_map[PLAYER.x+2][PLAYER.y].block_path:
    #             SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][walls],
    #                               (constants.M_Walls_Pos[walls]))
    #         if check_target(map_check_for_creatures(PLAYER.x+2, PLAYER.y, PLAYER),1):
    #             pass
    #
    #         if check_item(heck_for_items(PLAYER.x+2, PLAYER.y, PLAYER), 2,PLAYER.x+2, PLAYER.y):
    #             pass
    #
    # ##########
    #
    #         if GAME.current_map[PLAYER.x+1][PLAYER.y].block_path:
    #             SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][walls],
    #                               (constants.M_Walls_Pos[walls]))
    #         # if check_target(map_check_for_creatures(PLAYER.x+1, PLAYER.y, PLAYER),0):
    #         #     pass
    #
    #         if map_check_for_creatures(PLAYER.x+1, PLAYER.y, PLAYER):
    #             for obj in GAME.current_objects:
    #                 obj.draw_self_fpp(1)
    #
    #
    #         if check_item(heck_for_items(PLAYER.x + 1, PLAYER.y, PLAYER), 1, PLAYER.x + 1, PLAYER.y):
    #             pass
    # #########
    #         if GAME.current_map[PLAYER.x][PLAYER.y].block_path:
    #             SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][walls],
    #                               (constants.M_Walls_Pos[walls]))



        # if GAME.current_map[PLAYER.x + cd][PLAYER.y].block_path:
        #     SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
        #                       (constants.M_Walls_Pos[bc]))



    if PLAYER.facing == 2:
        if GAME.current_map[PLAYER.x + 1][PLAYER.y + 3].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][0],
                              (constants.L_Walls_Pos[0]))
        if check_target_L(map_check_for_creatures(PLAYER.x + 1, PLAYER.y + 3, PLAYER), 2):
            pass

        if check_item_L(heck_for_items(PLAYER.x+1, PLAYER.y + 3, PLAYER), 3, PLAYER.x+1, PLAYER.y +3):
            pass


        if GAME.current_map[PLAYER.x + 1][PLAYER.y + 2].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][1],
                              (constants.L_Walls_Pos[1]))
        if check_target_L(map_check_for_creatures(PLAYER.x + 1, PLAYER.y + 2, PLAYER), 1):
            pass

        if check_item_L(heck_for_items(PLAYER.x+1, PLAYER.y + 2, PLAYER), 2, PLAYER.x+1, PLAYER.y +2):
            pass

        if GAME.current_map[PLAYER.x + 1][PLAYER.y + 1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][2],
                              (constants.L_Walls_Pos[2]))
        if check_target_L(map_check_for_creatures(PLAYER.x + 1, PLAYER.y + 1, PLAYER), 0):
            pass
        if check_item_L(heck_for_items(PLAYER.x+1, PLAYER.y + 1, PLAYER), 1, PLAYER.x+1, PLAYER.y +1):
            pass


        if GAME.current_map[PLAYER.x + 1][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][3],
                              (constants.L_Walls_Pos[3]))

        if check_item_L(heck_for_items(PLAYER.x+1, PLAYER.y, PLAYER), 0, PLAYER.x+1, PLAYER.y):
            pass
        ## RIGHTIE

        if GAME.current_map[PLAYER.x - 1][PLAYER.y + 3].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][0],
                              (constants.R_Walls_Pos[0]))
        if check_target_R(map_check_for_creatures(PLAYER.x - 1, PLAYER.y + 3, PLAYER), 2):
            pass

        if check_item_R(heck_for_items(PLAYER.x-1, PLAYER.y + 3, PLAYER), 3, PLAYER.x-1, PLAYER.y +3):
            pass


        if GAME.current_map[PLAYER.x - 1][PLAYER.y + 2].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][1],
                              (constants.R_Walls_Pos[1]))
        if check_target_R(map_check_for_creatures(PLAYER.x - 1, PLAYER.y + 2, PLAYER), 1):
            pass
        if check_item_R(heck_for_items(PLAYER.x-1, PLAYER.y + 2, PLAYER), 2, PLAYER.x-1, PLAYER.y +2):
            pass

        if GAME.current_map[PLAYER.x - 1][PLAYER.y + 1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][2],
                              (constants.R_Walls_Pos[2]))
        if check_target_R(map_check_for_creatures(PLAYER.x - 1, PLAYER.y + 1, PLAYER), 0):
            pass

        if check_item_R(heck_for_items(PLAYER.x-1, PLAYER.y + 1, PLAYER), 1, PLAYER.x-1, PLAYER.y +1):
            pass

        if GAME.current_map[PLAYER.x - 1][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][3],
                              (constants.R_Walls_Pos[3]))

        if check_item_R(heck_for_items(PLAYER.x-1, PLAYER.y , PLAYER), 0, PLAYER.x-1, PLAYER.y):
            pass
        ## Center:

        if GAME.current_map[PLAYER.x][PLAYER.y + 3].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][0],
                              (constants.M_Walls_Pos[0]))
        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y + 3, PLAYER), 2):
            pass

        if check_item(heck_for_items(PLAYER.x, PLAYER.y + 3, PLAYER), 3, PLAYER.x, PLAYER.y +3):
            pass


        if GAME.current_map[PLAYER.x][PLAYER.y + 2].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][1],
                              (constants.M_Walls_Pos[1]))
        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y + 2, PLAYER), 1):
            pass

        if check_item(heck_for_items(PLAYER.x, PLAYER.y + 2, PLAYER), 2, PLAYER.x, PLAYER.y +2):
            pass

        if GAME.current_map[PLAYER.x][PLAYER.y + 1].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][2],
                              (constants.M_Walls_Pos[2]))
        if check_target(map_check_for_creatures(PLAYER.x, PLAYER.y + 1, PLAYER), 0):
            pass

        if check_item(heck_for_items(PLAYER.x, PLAYER.y + 1, PLAYER), 1, PLAYER.x, PLAYER.y +1):
            pass
        if GAME.current_map[PLAYER.x][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][3],
                              (constants.M_Walls_Pos[3]))


        #
        #
        # if GAME.current_map[PLAYER.x + 1][PLAYER.y + cd].block_path:
        #     SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],
        #                       (constants.L_Walls_Pos[bc]))
        # if GAME.current_map[PLAYER.x - 1][PLAYER.y + cd].block_path:
        #     SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
        #                       (constants.R_Walls_Pos[bc]))
        # if GAME.current_map[PLAYER.x][PLAYER.y + cd].block_path:
        #     SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
        #                       (constants.M_Walls_Pos[bc]))



    if PLAYER.facing == 3:

        #leftie
        if GAME.current_map[PLAYER.x-3][PLAYER.y +1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][0],
                                    (constants.L_Walls_Pos[0]))
        if check_target_L(map_check_for_creatures(PLAYER.x-3, PLAYER.y + 1, PLAYER), 2):
            pass

        if check_item_L(heck_for_items(PLAYER.x-3, PLAYER.y + 1, PLAYER), 3,PLAYER.x-3, PLAYER.y + 1):
            pass


        if GAME.current_map[PLAYER.x-2][PLAYER.y +1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                                    (constants.L_Walls_Pos[1]))
        if check_target_L(map_check_for_creatures(PLAYER.x-2, PLAYER.y + 1, PLAYER), 1):
            pass

        if check_item_L(heck_for_items(PLAYER.x-2, PLAYER.y + 1, PLAYER), 2,PLAYER.x-2, PLAYER.y + 1):
            pass

        if GAME.current_map[PLAYER.x-1][PLAYER.y +1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                                    (constants.L_Walls_Pos[2]))
        if check_target_L(map_check_for_creatures(PLAYER.x-1, PLAYER.y + 1, PLAYER), 0):
            pass

        if check_item_L(heck_for_items(PLAYER.x-1, PLAYER.y + 1, PLAYER), 1,PLAYER.x-1, PLAYER.y + 1):
            pass

        if GAME.current_map[PLAYER.x][PLAYER.y+1].block_path:
            SURFACE_MAIN.blit(constants.L_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                                    (constants.L_Walls_Pos[3]))


        if check_item_L(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 0,PLAYER.x, PLAYER.y - 1):
            pass


        ## IRGHTIE

        if GAME.current_map[PLAYER.x-3][PLAYER.y -1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][0],
                                    (constants.R_Walls_Pos[0]))
        if check_target_R(map_check_for_creatures(PLAYER.x-3, PLAYER.y - 1, PLAYER), 2):
            pass

        if check_item_R(heck_for_items(PLAYER.x-3, PLAYER.y - 1, PLAYER), 3,PLAYER.x-3, PLAYER.y - 1):
            pass


        if GAME.current_map[PLAYER.x-2][PLAYER.y -1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                                    (constants.R_Walls_Pos[1]))
        if check_target_R(map_check_for_creatures(PLAYER.x-2, PLAYER.y - 1, PLAYER), 1):
            pass

        if check_item_R(heck_for_items(PLAYER.x-2, PLAYER.y - 1, PLAYER), 2,PLAYER.x-2, PLAYER.y - 1):
            pass

        if GAME.current_map[PLAYER.x-1][PLAYER.y -1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                                    (constants.R_Walls_Pos[2]))
        if check_target_R(map_check_for_creatures(PLAYER.x-1, PLAYER.y - 1, PLAYER), 0):
            pass
        if check_item_R(heck_for_items(PLAYER.x-1, PLAYER.y - 1, PLAYER), 1,PLAYER.x-1, PLAYER.y - 1):
            pass
        if GAME.current_map[PLAYER.x][PLAYER.y-1].block_path:
            SURFACE_MAIN.blit(constants.R_Walls_flipper[
                                  ((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                                    (constants.R_Walls_Pos[3]))

        if check_item_R(heck_for_items(PLAYER.x, PLAYER.y - 1, PLAYER), 0,PLAYER.x, PLAYER.y - 1):
            pass


        # #centerie
        if GAME.current_map[PLAYER.x-3][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][0],
                              (constants.M_Walls_Pos[0]))
        if check_target(map_check_for_creatures(PLAYER.x-3, PLAYER.y, PLAYER),2):
            pass

        if check_item(heck_for_items(PLAYER.x-3, PLAYER.y, PLAYER), 3,PLAYER.x-3, PLAYER.y):
            pass

        if GAME.current_map[PLAYER.x-2][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][1],
                              (constants.M_Walls_Pos[1]))
        if check_target(map_check_for_creatures(PLAYER.x-2, PLAYER.y, PLAYER),1):
            pass

        if check_item(heck_for_items(PLAYER.x-2, PLAYER.y, PLAYER), 2,PLAYER.x-2, PLAYER.y):
            pass
        if GAME.current_map[PLAYER.x-1][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][2],
                              (constants.M_Walls_Pos[2]))
        if check_target(map_check_for_creatures(PLAYER.x-1, PLAYER.y, PLAYER),0):
            pass

        if check_item(heck_for_items(PLAYER.x-1, PLAYER.y, PLAYER), 1,PLAYER.x-1, PLAYER.y):
            pass
        if GAME.current_map[PLAYER.x][PLAYER.y].block_path:
            SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][3],
                              (constants.M_Walls_Pos[3]))

    if check_item(heck_for_items(PLAYER.x , PLAYER.y, PLAYER), 0,PLAYER.x , PLAYER.y):
        pass
            # if GAME.current_map[PLAYER.x - cd][PLAYER.y + 1].block_path:
            #     SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],(constants.L_Walls_Pos[bc]))
            # if GAME.current_map[PLAYER.x - cd][PLAYER.y -1].block_path:
            #     SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
            #                       (constants.R_Walls_Pos[bc]))
            # if GAME.current_map[PLAYER.x - cd][PLAYER.y].block_path:
            #     SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
            #                       (constants.M_Walls_Pos[bc]))




    ### DRAW MONSTERS

    ### DRAW DOORS/SECRET WALLS etc
    # for game_obj in GAME.current_objects:
    #     # if game_obj.sprite_anim and game_obj != PLAYER and game_obj.ai:
    #         if game_obj.sprite_anim and game_obj != PLAYER and not game_obj.name_object == "DOOR" and not game_obj.name_object == "Button":
    #             if len(game_obj.sprite_anim) > 1:
    #                 game_obj.crawl_sprite = game_obj.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
    #                 # game_obj.crawl_sprite = game_obj.sprite_anim[0]
    #         if game_obj.name_object == "BehoLol":
    #             game_obj.crawl_sprite = game_obj.sprite_anim_far[int((pygame.time.get_ticks() / 500) % 2)]

    ### DRAW ITEMS ON GROUND
    # for item_obj in GAME.interact_objects:
    #     if ((PLAYER.x + constants.P_controls_x[PLAYER.facing] == item_obj.x)
    #             and (PLAYER.y - constants.L_controls_y[PLAYER.facing] == item_obj.y)):
    #
    #         SURFACE_MAIN.blit(item_obj.f_sprite, (constants.Item_L_start))
    #     if PLAYER.x == item_obj.x and PLAYER.y == item_obj.y:
    #         SURFACE_MAIN.blit(item_obj.f_sprite, constants.Item_L_self)

    # draw_objects()

# def draw_fpp():
#     # TODO add left/right -2/+2 wall draws
#     # draw FLOOR !@#$!@#%
#     SURFACE_MAIN.blit(constants.G_Floor[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)], (16,400))
#     SURFACE_MAIN.blit(constants.G_Ceiling[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)], (16,16))
#
#     for bc, cd in zip(range(0, 4), constants.random_range):
#
#         if PLAYER.facing == 0:  # "N":
#             # for ab, bc in zip(range(0,-4,-1))
#                 # print("ab",ab)
#             # print("bc",bc)
#             # if GAME.current_map[PLAYER.x-1][PLAYER.y].block_path:
#             #     SURFACE_MAIN.blit(constants.L_Walls[3],(constants.L_Walls_Pos[3]))
#             if GAME.current_map[PLAYER.x-1][PLAYER.y -cd].block_path:
#                 SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],(constants.L_Walls_Pos[bc]))
#             # if game_.y == PLAYER.y -cd and game_ != PLAYER and game_.x == PLAYER.x:
#             #     SURFACE_MAIN.blit(game_.crawl_sprite, (constants.M_mid_monster))
#             if GAME.current_map[PLAYER.x+1][PLAYER.y-cd].block_path:
#                 SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],
#                                   (constants.R_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x][PLAYER.y - cd].block_path:
#                 SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],
#                                   (constants.M_Walls_Pos[bc]))
#
#
#
#         elif PLAYER.facing == 1:
#             if GAME.current_map[PLAYER.x + cd][PLAYER.y - 1].block_path:
#                 SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],(constants.L_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x + cd][PLAYER.y +1].block_path:
#                 SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.R_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x + cd][PLAYER.y].block_path:
#                 SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.M_Walls_Pos[bc]))
#
#
#
#         elif PLAYER.facing == 2:
#             if GAME.current_map[PLAYER.x + 1][PLAYER.y + cd].block_path:
#                 SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],
#                                   (constants.L_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x - 1][PLAYER.y + cd].block_path:
#                 SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.R_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x][PLAYER.y + cd].block_path:
#                 SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.M_Walls_Pos[bc]))
#
#
#             # for obj in GAME.current_objects:
#             #     obj.draw_in_fpp(PLAYER.x,PLAYER.y)
#
#         elif PLAYER.facing == 3:
#
#             if GAME.current_map[PLAYER.x - cd][PLAYER.y + 1].block_path:
#                 SURFACE_MAIN.blit(constants.L_Walls_flipper[((PLAYER.x+PLAYER.y+PLAYER.facing)%2)][bc],(constants.L_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x - cd][PLAYER.y -1].block_path:
#                 SURFACE_MAIN.blit(constants.R_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.R_Walls_Pos[bc]))
#             if GAME.current_map[PLAYER.x - cd][PLAYER.y].block_path:
#                 SURFACE_MAIN.blit(constants.M_Walls_flipper[((PLAYER.x + PLAYER.y + PLAYER.facing) % 2)][bc],
#                                   (constants.M_Walls_Pos[bc]))
#
#
#
#
#     ### DRAW MONSTERS
#
#     ### DRAW DOORS/SECRET WALLS etc
#     # for game_obj in GAME.current_objects:
#     #     # if game_obj.sprite_anim and game_obj != PLAYER and game_obj.ai:
#     #         if game_obj.sprite_anim and game_obj != PLAYER and not game_obj.name_object == "DOOR" and not game_obj.name_object == "Button":
#     #             if len(game_obj.sprite_anim) > 1:
#     #                 game_obj.crawl_sprite = game_obj.sprite_anim[int((pygame.time.get_ticks() / 500) % 2)]
#     #                 # game_obj.crawl_sprite = game_obj.sprite_anim[0]
#     #         if game_obj.name_object == "BehoLol":
#     #             game_obj.crawl_sprite = game_obj.sprite_anim_far[int((pygame.time.get_ticks() / 500) % 2)]
#
#     ### DRAW ITEMS ON GROUND
#     for item_obj in GAME.interact_objects:
#         if ((PLAYER.x + constants.P_controls_x[PLAYER.facing] == item_obj.x)
#                 and (PLAYER.y - constants.L_controls_y[PLAYER.facing] == item_obj.y)):
#
#             SURFACE_MAIN.blit(item_obj.f_sprite, (constants.Item_L_start))
#         if PLAYER.x == item_obj.x and PLAYER.y == item_obj.y:
#             SURFACE_MAIN.blit(item_obj.f_sprite, constants.Item_L_self)
#
#     draw_objects()

def draw_UI():
    pygame.draw.rect(SURFACE_MAIN, constants.COLOR_BLACK, (800, 10, 500, 700))
    ## Inventory Draw
    for n in range(0,8):
        SURFACE_MAIN.blit(constants.INV_ICON, (n * 50 + 20, 659))

    for obj in PLAYER.container.inventory:
        if None:
            SURFACE_MAIN.blit(constants.INV_ICON, (1 * 50 + 20, 659))
        for n in range(0, len(PLAYER.container.inventory)):
            if obj:
                SURFACE_MAIN.blit(PLAYER.container.inventory[n].i_sprite, (n*50+20 , 659))
            else:

                SURFACE_MAIN.blit(constants.INV_ICON, (n * 50 + 20, 659))

    ## DRAW UI
    SURFACE_MAIN.blit(constants.SZABLON_LOL,(0,0))
    SURFACE_MAIN.blit(constants.right_ui,(ASSETS.right_ui_posx,ASSETS.right_ui_posy))
    SURFACE_MAIN.blit(ASSETS.SpellBook,(ASSETS.right_ui_posx+10,ASSETS.right_ui_posy+50))
    SURFACE_MAIN.blit(constants.IMG_Portrait1,(ASSETS.hero_face,ASSETS.right_ui_posy))
    if not PLAYER.creature.gear.i_sprite:
        SURFACE_MAIN.blit(constants.UI_Fist,
                          (ASSETS.right_ui_posx + 10, ASSETS.right_ui_posy + ASSETS.SpellBook.get_height() + 50))

    else:
        SURFACE_MAIN.blit(PLAYER.creature.gear.i_sprite,
                      (ASSETS.right_ui_posx + 10, ASSETS.right_ui_posy + ASSETS.SpellBook.get_height() + 50))
    draw_map(GAME.current_map)

####################################

##              HELPER           ###

####################################

def helper_text_objects(incoming_text, incoming_color, incoming_background):
    if incoming_background:
        Text_surface = ASSETS.FONT_MESSAGE_TEXT.render(incoming_text,False,incoming_color, incoming_background)

    else:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text,False,incoming_color)

    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):
    font_object = font.render ('a', False, (0,0,0))
    font_rect = font_object.get_rect()

    return font_rect.height

def helper_text_width(font):
    font_object = font.render('a', False, (0,0,0))
    font_rect = font_object.get_rect()
    return font_rect.width

def spell_helper(sprite):
    local_surface = SURFACE_MAIN
    spellcast = True
    while spellcast:
        for sprites in range (0,16):
            randy = tcod.random_get_int(0,150,450)
            randx = tcod.random_get_int(0,200,500)
            randy2 = tcod.random_get_int(0,150,450)
            randx2 = tcod.random_get_int(0,200,500)
            randy3 = tcod.random_get_int(0,150,450)
            randx3 = tcod.random_get_int(0,200,500)
            # randy4 = tcod.random_get_int(0,150,450)
            # randx4 = tcod.random_get_int(0,200,500)
            for x in range(len(sprite)):
                SURFACE_MAIN.blit(sprite[x], (randx,randy))
                SURFACE_MAIN.blit(sprite[x], (randx2,randy2))
                SURFACE_MAIN.blit(sprite[x], (randx3,randy3))
                # SURFACE_MAIN.blit(constants.poison[x], (randx4,randy4))
                # continue

                pygame.display.update()
                # time.sleep(anim_delay)
                draw_game()
        spellcast = False

def door_helper(door,type):
    #door.ai = None
    anim_speed = 0.1
    if type == "Door":
        y = None
        if door.status == "Closed" or door.status == "Locked":
            game_message("Door opened!", constants.COLOR_WHITE)
            GAME.current_map[door.x][door.y].door_path = False
            door.status ="Open"
            constants.door_open.play()
            door.sprite = constants.door_o
            y  =range(len(door.sprite_anim))

        elif door.status == "Open":
            game_message("Door Closed!", constants.COLOR_WHITE)
            GAME.current_map[door.x][door.y].door_path = True
            door.status ="Closed"
            constants.door_close.play()
            door.sprite = constants.door_c
            y = reversed(range(len(door.sprite_anim)))
        if y:

            for x in y:

                door.crawl_sprite = door.sprite_anim[x]
                draw_game()
                time.sleep(anim_speed)

    elif type == "Button":

        game_message("Button pressed!!", constants.COLOR_WHITE)
        GAME.current_map[door.x][door.y].block_path = False
        door.crawl_sprite = constants.wall_button_bc1
        GAME.current_objects.remove(door)
    elif type == "Wall":

            game_message("Wall! BEGONE!", constants.COLOR_WHITE)

            GAME.current_map[door.x][door.y].block_path = False

            GAME.current_objects.remove(door)
    else:
        print("Check the code")


def game_main_loop():
    game_quit = False
    t = time.time()
    # player_action = "no-action"

    while not game_quit:

        # player action definition

        # handle player input
        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        # if time.time() >t +1:
        #     t = time.time()
        #     for obj in GAME.current_objects:
        #         if obj.ai:
        #             obj.ai.take_turn()
        # elif player_action != "no-action":
        #


        ### process INPUT

        draw_game()
        CLOCK.tick(constants.GAME_FPS)

    pygame.quit()
    exit()


###############################################################
###                     GAME INITS                          ###
###############################################################

def monsters_init():
    ## Items used by monsters / in containers

    # def __init__(self,
    #              x: Any = None,
    #              y: Any = None,
    #              name: str = "PlaceholderName",
    #              type: str = "Typeless",
    #              power: int = 1,
    #              effect: Any = None,
    #              weight: Any = None,
    #              i_sprite: str = "",
    #              f_sprite: str = "") -> None


    P_Weapon3 = obj_Items(None, None,"Ax","1H",200,None,None,constants.L_Axe, constants.L_Axe_f)
    P_Weapon_Stick = obj_Items(None,None, "Staff","1h", 25, None,None,constants.L_Staff,constants.L_Wand)
    P_Key = obj_Items(10,12,"Moon Key","Item", 0, None, None, constants.P_Key, constants.P_Key)

    ## Items on ground
    # Define items here



    # Append GAME.interact_objects with all of them here:



    ## MONSTER


    # item_com1 = com_Item(value=54, use_function=cast_heal, name="Staff", target="self", i_sprite =constants.L_Staff,
    #                      f_sprite= constants.L_Wand)
    # item_sword1 = com_Item(value=10, use_function=None, name="Sword", target=None,
    #                        i_sprite=constants.L_Sword_I, f_sprite=constants.L_Sword_F)
    # item_com_dummy = com_Item(value=0.0,name=None,target=None,i_sprite=constants.INV_ICON,f_sprite=None)

    ai_com = ai_Test()
    ai_aggo = ai_Aggro()
    P_Creature_Sharga = com_Creature("Paint Monster",
                                     object_type="Monster",
                                     hp=20,
                                     death_function=death_monster,
                                     gear=P_Weapon3)

    ENEMY = obj_Actor(x= 11, y=3, facing=3, name_object="BehoLol",
                      sprite=constants.S_ENEMY,
                      sprite_anim_far=constants.S_BEHO_ANIM2,
                      sprite_anim= constants.S_BEHO_ANIM,
                      creature=P_Creature_Sharga,
                      ai=ai_com,
                      crawl_sprite=constants.S_BEHO_LOL,
                      item=None,
                      type="Monster")

    # P_Creature_Sharga2 = com_Creature("Paint Monster",
    #                                  object_type="Monster",
    #                                  hp=20,
    #                                  death_function=death_monster,
    #                                  gear=None)
    # ai_com2 = ai_Test()
    # ENEMI = obj_Actor(1, 2, 3, "BehoLol",
    #                   constants.S_ENEMY,
    #                   sprite_anim=[constants.S_BEHO_LOL,
    #                                constants.S_BEHO_LOL2],
    #                   creature=P_Creature_Sharga2,
    #                   ai=ai_com2,
    #                   crawl_sprite=constants.S_SHARGA,
    #                   item=None)
    # GAME.next_lvl.append(ENEMI)
    #
    # CHEST
    item_com2 = com_Item(value=150,use_function=cast_thunder,name="Book",i_sprite = constants.I_SpellBook,
                         f_sprite=constants.L_Spell)
    ai_com2 = ai_Test()


    P_Chest = com_Creature("Chest",object_type="Container",death_function= death_monster,gear=P_Weapon_Stick)
    CHEST = obj_Actor(11, 4,2, "Chest",
                      constants.P_CHEST_M,
                      sprite_anim=[constants.P_CHEST,
                                   constants.P_CHESTi],
                      creature=P_Chest,
                      ai = None,
                      crawl_sprite=constants.P_CHEST,
                      container=None,
                      item=item_com2,
                      type="Chest")
    global GAME_GEAR
    GAME_GEAR = []
    GAME.current_objects.append(ENEMY)
    GAME.current_objects.append(CHEST)
    GAME.interact_objects.append(P_Key)
    # GAME.current_objects.append(item_com_dummy)
    GAME_GEAR.append(None)



def spellList():
    ticks = int(pygame.time.get_ticks() / 1000)
    spell_thunder = all_spells("Thunder", 25,1, True, "spellcast",constants.thunder) # spell name, spell power, cast type, sprite
    spell_heal = all_spells("Heal", 35,1, True, "self_heal")
    spell_fire = all_spells("Poison Blast", 10, 1, True,"spellcast",constants.poison)
    SPELLBOOK.append(spell_thunder)
    SPELLBOOK.append(spell_heal)
    SPELLBOOK.append(spell_fire)


def interactables_init():
    # ai3 = ai_Doors()

    ## CLOSED DOORS

    door1 = com_Creature("Door1","Door",death_function=death_monster, type="Door")
    DOOR_L1_1 = obj_Actor(
                        x = 14,
                        y = 5,
                        facing = 2,
                        name_object = "DOOR",
                        sprite = constants.door_c,
                        crawl_sprite = constants.door1_mid,
                        sprite_anim = [constants.door1_mid,constants.door2_mid,constants.door3_mid,constants.door4_mid, constants.door1_o_mid],
                        creature = door1, #door , # class
                        container = None, # class
                        item = None, # class
                        status= "Closed",
                        ai = None,
                        type = "Door"
                        )
    GAME.current_objects.append(DOOR_L1_1)

    door2 = com_Creature("Door2","Door",death_function=death_monster, type="Door")
    DOOR_L1_2 = obj_Actor(
                        x = 22,
                        y = 13,
                        facing = 2,
                        name_object = "DOOR",
                        sprite = constants.door_c,
                        crawl_sprite = constants.door1_mid,
                        sprite_anim = [constants.door1_mid,constants.door2_mid,constants.door3_mid,constants.door4_mid, constants.door1_o_mid],
                        creature = door2, #door , # class
                        container = None, # class
                        item = None, # class
                        status= "Closed",
                        ai = None,
                        type = "Door"

                        )
    GAME.current_objects.append(DOOR_L1_2)



    # LOCKED DOORS
    door_l_1 = com_Creature("Moon Door","Door",death_function=death_monster, type="Door")
    DOOR_L1_L_1 = obj_Actor(
                        x = 16,
                        y = 5,
                        facing = 1,
                        name_object = "DOOR",
                        sprite = constants.door_c,
                        crawl_sprite = constants.door1_mid,
                        sprite_anim = [constants.door1_mid,constants.door2_mid,constants.door3_mid,constants.door4_mid, constants.door1_o_mid],
                        creature = door_l_1, #door , # class
                        container = None, # class
                        item = "Moon Key", # class
                        status= "Locked",
                        ai = None,
                        type = "Door"

                        )
    GAME.current_objects.append(DOOR_L1_L_1)
    # ai4= ai_Doors()



    door_l_2 = com_Creature("Door2","Door",death_function=death_monster, type="Door")
    DOOR_L1_2 = obj_Actor(
                        x = 7,
                        y = 15,
                        facing = 2,
                        name_object = "DOOR",
                        sprite = constants.door_c,
                        crawl_sprite = constants.door1_mid,
                        sprite_anim = [constants.door1_mid,constants.door2_mid,constants.door3_mid,constants.door4_mid, constants.door1_o_mid],
                        creature = door_l_2, #door , # class
                        container = None, # class
                        item = "Ogre Key", # class
                        status= "Locked",
                        ai = None,
                        type = "Door"

                        )
    GAME.current_objects.append(DOOR_L1_2)



    ## Other button Doors
    door_l_p1 = com_Creature("Door","Door",death_function=death_monster, type="Door")
    DOOR_L1_p1 = obj_Actor(
                        x = 26,
                        y = 16,
                        facing = 2,
                        name_object = "DOOR",
                        sprite = constants.door_c,
                        crawl_sprite = constants.door1_mid,
                        sprite_anim = [constants.door1_mid,constants.door2_mid,constants.door3_mid,constants.door4_mid, constants.door1_o_mid],
                        creature = door_l_p1, #door , # class
                        container = None, # class
                        item = None, # class
                        status= "Locked",
                        ai = None,
                        type = "Door"

                        )
    GAME.current_objects.append(DOOR_L1_p1)



    ###

    #P1 door opener

    # button_l1 = com_Creature("Button","Button",death_function=None, type="Button")
    # Button_l1_01 = obj_Actor(
    #                     x = 28,
    #                     y = 14,
    #                     facing = 1,
    #                     name_object = "Button",
    #                     sprite = constants.m_button,
    #                     crawl_sprite = constants.wall_button_bc,
    #                     sprite_anim = [constants.wall_button_bc,constants.wall_button_bc1],
    #                     creature = button_l1, #door , # class
    #                     container = None, # class
    #                     item = None, # class
    #                     status= "Closed",
    #                     ai = None,
    #                     target_obj=DOOR_L1_p1
    #                     )
    #
    #
    # GAME.current_objects.append(Button_l1_01)

    wall = com_Creature("Wall","Secret",death_function=None, type="Wall")
    F_Wall_01 = obj_Actor(
                        x = 11,
                        y = 17,
                        facing = 3,
                        name_object = "Wall",
                        sprite = constants.m_button,
                        crawl_sprite = constants.wall1_mid,
                        sprite_anim = [constants.wall1_mid],
                        creature = wall, #door , # class
                        container = None, # class
                        item = "Key", # class
                        status= "Open",
                        ai = None,
                        type = "Wall"

                        )




    GAME.current_objects.append(F_Wall_01)

    button = com_Creature("Button","Button",death_function=None, type="Button")
    Button_01 = obj_Actor(
                        x = 18,
                        y = 16,
                        facing = 1,
                        name_object = "Button",
                        sprite = constants.m_button,
                        crawl_sprite = constants.wall_button_bc,
                        sprite_anim = [constants.wall_button_bc,constants.wall_button_bc1],
                        creature = button, #door , # class
                        container = None, # class
                        item = None, # class
                        status= "Closed",
                        ai = None,
                        target_obj=F_Wall_01,
                        type = "Wall"
                        )


    GAME.current_objects.append(Button_01)
    for obj in GAME.current_objects:
        if obj.crawl_sprite == constants.door1_mid:
            GAME.current_map[obj.x][obj.y].door_path = True
        # if obj.crawl_sprite == constants.wall_button:
        #     GAME.current_map[obj.x][obj.y].button_path = True

        else:

            GAME.current_map[obj.x][obj.y].door_path = False





def game_initialize():

    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ASSETS
    global SHEET_ONE
    global SPELLBOOK
    global GAME_INTERACTS
    global MOUSE
    # global ENEMI

    # global ENEMY, CHEST
    pygame.init()

    pygame.key.set_repeat(500,70) # key repeat function (after ms, repeat every ms)

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                            constants.GAME_HEIGHT))
    SPELLBOOK = []
    MOUSE = []
    GAME = obj_Game()
    monsters_init()
    interactables_init()
    spellList()
    



    #SPELLBOOK = ["HEAL","THUNDER", "FIREBALL(tm)","DMGBOOST(tm)"]
    #GAME.current_map = map_create()
    #GAME.message_history = []
    #SHEET_ONE = obj_SpriteSheet("sheets/sheet_2.png")

    CLOCK = pygame.time.Clock()
    FOV_CALCULATE = True

    ## TEMP SPRITES ##

    ASSETS = struc_Assets()

    ## Item Related

    container_com1 = com_Container()
    P_Weapon1 = com_Weapon("Sword")
    P_Weapon2 = obj_Items(None,None,"Test Weapon2","1H",20,None,None, constants.L_Axe, constants.L_Spell)
    P_Bare_Hand = obj_Items(None, None, "Fist", "1H", 10, None, None, constants.UI_Fist, None)

    ## PLAYER
    # Creature
    P_Creature_Player = com_Creature("MaeL",
                                     object_type="Player",
                                     hp=25,
                                     #gear=P_Weapon2)
                                     gear=P_Bare_Hand)

    # ACTOR
    PLAYER = obj_Actor(10, 3, 2, "Player",
                       constants.S_PLAYER_DOWN,
                       creature=P_Creature_Player,
                       sprite_anim=None,
                       crawl_sprite=None,
                       container=container_com1,
                        type = "Player")


    # P_Creature_Sharga2 = com_Creature("Paint Monster",
    #                                  object_type="Monster",
    #                                  hp=20,
    #                                  death_function=death_monster,
    #                                  gear=None)



    GAME_INTERACTS = []

    GAME.current_objects.append(PLAYER)
    GAME_INTERACTS.append(P_Bare_Hand)

def game_message(game_msg, msg_color=constants.COLOR_WHITE):
    GAME.message_history.append((game_msg, msg_color))
    pygame.display.update()

def game_handle_keys():
    events_list = pygame.event.get()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global FOV_CALCULATE

    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN:

#########################
###                   ###
###     TEST KEYS     ###
###                   ###
#########################
            # r t y u i o f j k l z x
            if event.key == pygame.K_c:
                # print(f"Player name: {PLAYER.name_object}")
                # pygame.mouse.set_visible(False)
                # None
                pass


            if event.key == pygame.K_z:
                pass

            if event.key == pygame.K_f:
                pass

            if event.key == pygame.K_j:
                pass

            if event.key == pygame.K_k:
                pass

            if event.key == pygame.K_v:
                pass

            if event.key == pygame.K_b:
                for x in constants.random_range:
                    print (x)
                pass

            if event.key == pygame.K_n:
                # GAME.current_map[PLAYER.x][PLAYER.y-1].wall_alcove = True
                abc = 0
                bcd =[]
                # for x in range(0, constants.MAP_WIDTH):
                #     for y in range(0, constants.MAP_HEIGHT):
                #         if GAME.current_map[x][y].door_path:
                #             abc += 1
                #             bcd.append(f'Test at x:{x}, y:{y}')

                print(abc)
                print(bcd)
                AlcoveL1 = com_Creature("Alcove","Alcove",death_function=death_monster, type="Alcove")
                # alc_x = PLAYER.x+PLAYER.facing
                DOOR_ZZ = obj_Actor(
                    x=PLAYER.x+PLAYER.facing,
                    y=PLAYER.y,
                    facing=0,
                    name_object="DOOR",
                    sprite=constants.door_c,
                    crawl_sprite=constants.alcove,
                    sprite_anim=[constants.door1_mid, constants.door2_mid, constants.door3_mid,
                                 constants.door4_mid, constants.door1_o_mid],
                    creature=AlcoveL1,  # door , # class
                    container=None,  # class
                    item=None,  # class
                    status="Locked",
                    ai=None
                        )
                GAME.current_map[DOOR_ZZ.x][DOOR_ZZ.y].wall_alcove = True
                GAME.current_objects.append(DOOR_ZZ)
                pass

            # if event.key == pygame.K_b:
            #     pass
            #     # for n in range(len(PLAYER.container.inventory)):
                #     xz = (PLAYER.container.inventory[n].item.name)
                #     if constants.Weapons.get(PLAYER.container.inventory[n].item.name):
                #         PLAYER.creature.gear.att = constants.Weapons.get(xz)
                #         game_message(("Weapon changed to " + PLAYER.container.inventory[n].item.name),constants.COLOR_RED)
                #         game_message(("Power changed to "+ str(PLAYER.creature.gear.att)),)
                #         ASSETS.Sword = PLAYER.container.inventory[n].item.i_sprite
                #         break





            # if event.key == pygame.K_v:
            #     pass
                # objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)
                # for obj in reversed(objects_at_player):
                #     if obj.item and obj.item != None:
                #         # obj.item.mouse_pick_up(MOUSE)
                #         print(obj)
                #         return "player-moved"
                #     else:
                #         print("Nothing to pick up!")
                #         return "player-moved"



#########################
###                   ###
###       Other       ###
###                   ###
#########################

            if event.key == pygame.K_m:
                big_map(GAME.current_map)


            # TURNING

            if event.key == pygame.K_e:
                if PLAYER.facing == 3:
                    PLAYER.facing = 0
                else:
                    PLAYER.facing += 1
                PLAYER.sprite = ASSETS.SHEET_ONE.get_image('a', PLAYER.facing, 16, 16, ())

                return "no-action"
            if event.key == pygame.K_q:
                if PLAYER.facing == 0:
                    PLAYER.facing = 3
                else:
                    PLAYER.facing -= 1
                PLAYER.sprite = ASSETS.SHEET_ONE.get_image('a', PLAYER.facing, 16, 16, ())


                return "no-action"

            ### MOVEMENT

            if event.key == pygame.K_w:
                PLAYER.creature.move(constants.L_controls_x[PLAYER.facing - 2], constants.L_controls_y[PLAYER.facing - 2])
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_s:
                PLAYER.creature.move(constants.L_controls_x[PLAYER.facing], constants.L_controls_y[PLAYER.facing])
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_d:
                PLAYER.creature.move(constants.L_controls_x[PLAYER.facing - 1], constants.L_controls_y[PLAYER.facing - 1])
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_a:
                PLAYER.creature.move(constants.L_controls_x[PLAYER.facing - 3], constants.L_controls_y[PLAYER.facing - 3])
                FOV_CALCULATE = True
                return "player-moved"



            #########################
            ###                   ###
            ### ITEM MANIPULATION ###
            ###                   ###
            #########################
            if event.key == pygame.K_g:
                x = 0
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)
                for obj in reversed(objects_at_player):
                    if obj and obj != None:
                        obj.pick_op(PLAYER)
                        return "player-moved"
                    else:
                        game_message("Something went wrong, check code")
                        return "player-moved"


            if event.key == pygame.K_h:
                # pass
                if len(PLAYER.container.inventory)>0:
                    PLAYER.container.inventory[-1].drop_down(PLAYER.x,PLAYER.y)

            if event.key == pygame.K_p:
                #menu_two()
                menu_inventory()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 or event.button == 3:
                if mouse_click(mouse_x, mouse_y, event.button) == "actioned":
                    return "player-moved"

    return "no-action"

def big_map(map_to_draw):
    map_close = False
    window_width = constants.GAME_WIDTH
    window_height = constants.GAME_HEIGHT
    SURFACE_MAIN.blit(constants.krycie, (0, 0))
    game_message(f'MAP LOADED')
    map_width = constants.map2_w*16
    map_height = constants.map2_h*16

    map_width_x = (window_width / 2) - (map_width / 2)
    map_height_y = (window_height / 2) - (map_height / 2)

    local_surface = pygame.Surface((map_width, map_height))

    while not map_close:
        # obj_list = []
        # Clear surface + BG color

        local_surface.fill(constants.COLOR_GRAY)
        pygame.draw.rect(SURFACE_MAIN, constants.COLOR_BLACK, (0, constants.GAME_HEIGHT - 65, constants.GAME_WIDTH, 50))

        SURFACE_MAIN.blit(local_surface, (map_width_x, map_height_y))
        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_rel = int(mouse_x - map_width_x)
        mouse_y_rel = int(mouse_y - map_height_y)

        draw_center(SURFACE_MAIN, "Object: ",
                  (20, constants.GAME_HEIGHT - 55), constants.COLOR_YELLOW)

        for x in range(0, constants.MAP_WIDTH):
            for y in range(0,constants.MAP_HEIGHT):
                is_visible = tcod.map_is_in_fov(FOV_MAP,x,y)
                if is_visible:
                    map_to_draw[x][y].explored = True
                    if map_to_draw[x][y].block_path:
                        # Draw Wall
                        SURFACE_MAIN.blit(constants.S_WALL,(map_width_x+x*16, map_height_y+y*16))

                    elif map_to_draw[x][y].block_path == False and x < 0 + constants.MAP_WIDTH and y < constants.MAP_HEIGHT:
                        # Draw floor
                        SURFACE_MAIN.blit(constants.S_FLOOR,(map_width_x+x*16, map_height_y+y*16))
        #
                elif map_to_draw[x][y].explored:
                    if map_to_draw[x][y].block_path == True:
                        # Draw Wall
                        SURFACE_MAIN.blit(constants.S_WALL_EX,(map_width_x+x*16, map_height_y+y*16))
                    elif map_to_draw[x][y].block_path == False and x < 0 + constants.MAP_WIDTH and y < constants.MAP_HEIGHT:
                        # Draw floor
                        SURFACE_MAIN.blit(constants.S_FLOOR_EX,(map_width_x+x*16, map_height_y+y*16))


        for event in events_list:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                map_close = True


        for obj in GAME.current_objects:
            obj.draw_on_map()
            is_visible = tcod.map_is_in_fov(FOV_MAP, obj.x, obj.y)
            if int(mouse_x_rel / 16) == obj.x and int(mouse_y_rel / 16) == obj.y and is_visible:
                if obj.creature.object_type == "Monster" or obj.creature.object_type == "Player":
                    draw_center(SURFACE_MAIN, f'Object: {obj.creature.name_instance} at x:{obj.x}, y:{obj.y}',
                              (20, constants.GAME_HEIGHT - 55), constants.COLOR_YELLOW)

                elif obj.creature.object_type != "Monster" and obj.creature.object_type != "Secret":
                    draw_center(SURFACE_MAIN, f'Object: {obj.creature.name_instance} at x:{obj.x}, y:{obj.y}!',
                              (20, constants.GAME_HEIGHT - 55), constants.COLOR_YELLOW)
            # elif int(mouse_x_rel / 16) != obj.x and int(mouse_y_rel / 16) != obj.y:
            #     draw_left(SURFACE_MAIN, "No object selected",
            #               (20, constants.GAME_HEIGHT - 55), constants.COLOR_GREEN)

                # print (obj.creature.name_instance)
            # else:
            #     draw_left(SURFACE_MAIN, "Object:                      ", (40,20), constants.COLOR_YELLOW)

            #     draw_map_items = ""

        # for obj in GAME.current_objects:
        #     if int(mouse_x_rel/16) == obj.x and obj.creature.name_instance != "MaeL":
        #         print(obj.creature.name_instance)
        # draw_map_items(obj_list)
        CLOCK.tick(constants.GAME_FPS)

        # pygame.display.flip()


        pygame.display.update()


def spellbook():


    menu_close = False
    game_draw = False
    window_width = constants.GAME_WIDTH
    window_height = constants.GAME_HEIGHT

    menu_width = 300
    menu_height = 300
    menu_text_font = ASSETS.FONT_MESSAGE_TEXT
    menu_text_height = helper_text_height(menu_text_font)
    menu_text_color = constants.COLOR_RED
    menu_size_x = (window_width / 2) - (menu_width / 2)
    menu_size_y = (window_height / 2) - (menu_height / 2)

    local_surface = pygame.Surface((menu_width, menu_height))



    while not menu_close:
        currentTick = int(pygame.time.get_ticks() / 1000)
        # Clear surface + BG color
        local_surface.fill(constants.COLOR_BLACK)
        draw_messages()
        # Get Mouse
        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_rel = int(mouse_x - menu_size_x)
        mouse_y_rel = int(mouse_y - menu_size_y)

        mouse_in_box = (0 <= mouse_x_rel <= menu_width and
                        0 <= mouse_y_rel <= menu_height)
        mouse_line_selection = int(mouse_y_rel / menu_text_height)

        # TODO register changes

        # print_list = [obj.item.name for obj in PLAYER.container.inventory]

        x = 0
        #
        # for spells in SPELLBOOK:

        pygame.display.flip()
        for spells in SPELLBOOK:
            if spells.cooldown > currentTick:
                spells.isActive = False
            elif spells.cooldown < currentTick and not spells.isActive:
                spells.isActive = True
                game_message(f'{spells.spell_name} ready')


            if spells.isActive :
                if x < len(SPELLBOOK) and x == mouse_line_selection and mouse_in_box:

                    draw_left(local_surface, spells.spell_name,
                              (5, 0 + (x * menu_text_height)),
                              constants.COLOR_BLACK,constants.COLOR_WHITE)
                else:
                    draw_left(local_surface, spells.spell_name,
                              (5, 0 + (x * menu_text_height)),
                              menu_text_color)
                x += 1

            else:
                draw_left(local_surface, "NOT AVAILABLE",
                                  (5, 0 + (x * menu_text_height)),
                                  menu_text_color)
                x += 1


        for event in events_list:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if mouse_in_box and mouse_line_selection < len(SPELLBOOK) and SPELLBOOK[mouse_line_selection].isActive:
                        PLAYER.creature.spellcast(SPELLBOOK[mouse_line_selection].spell_dmg,
                                                  SPELLBOOK[mouse_line_selection].cast_type,
                                                  SPELLBOOK[mouse_line_selection].spell_sprite,
                                                  SPELLBOOK[mouse_line_selection].spell_name
                                                  )
                        menu_close = True
                        SPELLBOOK[mouse_line_selection].cooldown = currentTick+8

                    elif mouse_in_box and not mouse_line_selection < len(SPELLBOOK):
                        None
                    elif mouse_in_box and mouse_line_selection < len(SPELLBOOK) and not SPELLBOOK[mouse_line_selection].isActive:
                        game_message("Spell not ready!", constants.COLOR_WHITE)
                    else:
                        game_message("SpellBook closed",constants.COLOR_WHITE)
                        return "QUIT"
                # if event.button == 3:
                #     PLAYER.container.inventory[mouse_line_selection].item.drop_down(PLAYER.x, PLAYER.y)
                #     menu_close = True

        # DRAW list

            # Display Menu
        pygame.display.flip()
        SURFACE_MAIN.blit(local_surface, (menu_size_x, menu_size_y))

        CLOCK.tick(constants.GAME_FPS)


def menu_inventory():

    menu_close = False
    game_draw = False
    window_width = constants.GAME_WIDTH
    window_height = constants.GAME_HEIGHT

    menu_width = 300
    menu_height = 300
    menu_text_font = ASSETS.FONT_MESSAGE_TEXT
    menu_text_height = helper_text_height(menu_text_font)
    menu_text_color = constants.COLOR_RED
    menu_size_x = (window_width/2) - (menu_width/2)
    menu_size_y = (window_height/2) - (menu_height/2)

    local_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        # Clear surface + BG color
        local_surface.fill(constants.COLOR_BLACK)
        draw_messages()
        # Get Mouse
        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_rel = int(mouse_x - menu_size_x)
        mouse_y_rel = int(mouse_y - menu_size_y)

        mouse_in_box = (0 <= mouse_x_rel <= menu_width and
                        0 <= mouse_y_rel <= menu_height)
        mouse_line_selection = int(mouse_y_rel / menu_text_height)

        # TODO register changes

        #print_list = [obj.name_object for obj in PLAYER.container.inventory]
        print_list = [obj.item.name for obj in PLAYER.container.inventory]
        #print_list.append("Items:")
        for line, (name) in enumerate((print_list)):
            if line == mouse_line_selection and mouse_in_box:
                draw_left(local_surface, name,
                      (5,0+(line*menu_text_height)),
                      menu_text_color, constants.COLOR_WHITE)
                    #print(menu_text_height)
            else:
                draw_left(local_surface, name,
                      (5,0+(line*menu_text_height)),
                      menu_text_color)

            line += 1



        for event in events_list:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_close = True

                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    draw_game()
                    if mouse_in_box and mouse_line_selection < len(print_list):
                        PLAYER.container.inventory[mouse_line_selection].item.use()

                        menu_close = True

                if event.button == 3:
                    if mouse_in_box and mouse_line_selection < len(print_list):
                        PLAYER.container.inventory[mouse_line_selection].item.drop_down(PLAYER.x, PLAYER.y)
                        menu_close = True

                        return "player-moved"
        # DRAW list



        # Display Menu
        SURFACE_MAIN.blit(local_surface, (menu_size_x,menu_size_y))



        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

if __name__ == '__main__':


    game_initialize()

    pygame.display.set_caption('MaeLs dank dung dung')
    pygame.display.set_icon(constants.L_Sword_F)
    game_main_loop()