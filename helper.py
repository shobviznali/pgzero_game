from pgzero.actor import Actor
from Game import LevelManager
from pgzero.rect import Rect
from AnimatedEnemys import AnimatedEnemyFlying, AnimatedEnemyWalking


start_button = Actor("main_menu/start.png", pos=(400, 200))
quit_button = Actor("main_menu/quit.png", pos=(400, 300))
sound_button = Actor("main_menu/sound_on.png", pos=(50, 50))
music_button = Actor('main_menu/music_off.png', pos=(750, 50))
pause_button = Actor('main_menu/pause.png', topright=(780, 20))
player = Actor("player/player_stand", pos=(30, 442))
bground = Actor("game_images/background/bgroudnd", topleft=(0, 0))
restart_button = Actor("main_menu/restart.png", topright=(780, 70))

# Creating our levels and level rects
levels = LevelManager(['./lvls/level1.json', './lvls/level2.json', './lvls/level3.json', './lvls/level4.json'])
level_rects = LevelManager(['./lvls/level1_rects.json', './lvls/level2_rects.json',
                            './lvls/level3_rects.json', './lvls/level4_rects.json'])


# Loading levels in lists and dict
def load_levels(cur_lev, cur_lev_rect):
    objects = []
    rects = []
    gems = {}
    enemy = []
    for object_name, object_data in cur_lev.items():
        if isinstance(object_data, dict) and "image" in object_data:
            # Loading gams seperate and etc
            if "gem" in object_name:
                gems[Actor(object_data['image'], pos=(object_data['coordinates_x'],
                                                      object_data['coordinates_y']))] = object_data['power']
            elif object_name == "enemy_walking":
                enemy1 = AnimatedEnemyWalking(object_data['image'], object_data['coordinates_x'],
                                              object_data["coordinates_y"], 1.5)
                enemy.append(enemy1)
            elif object_name == "enemy_flying":
                enemy1 = AnimatedEnemyFlying(object_data["image"], object_data["coordinates_x"],
                                             object_data["coordinates_y"], 5)
                enemy.append(enemy1)

            elif "coordinates" in object_data:
                for i in range(len(object_data['coordinates'])):
                    objects.append(Actor(object_data['image'], pos=object_data['coordinates'][i]))
            else:
                objects.append(Actor(object_data['image'], pos=(object_data['coordinates_x'],
                                                                object_data['coordinates_y'])))

    # Loading level rects so player can walk on that rects
    for object_name, object_data in cur_lev_rect.items():
        rects.append(Rect(object_data['x_1'], object_data['y_1'],
                          object_data['x_2'], object_data['y_2']))

    return objects, rects, gems, enemy
