import pgzrun
import warnings
import time
import variables
from helper import start_button, quit_button, sound_button, pause_button, restart_button
from helper import music_button, bground
from functions import start_game, quit_game, sound_on, music_on, jump_boost
from functions import inactive_boost
from helper import levels, level_rects
from helper import load_levels, player
warnings.filterwarnings("ignore")


WIDTH = 800
HEIGHT = 600
checkpoint_x, checkpoint_y = variables.poses[0]
menu_active = True
restart_level = False


# Function for updating first level
def first_level():
    if variables.first_level:
        # Getting our current level from our class object
        current_level = levels.get_current_level()
        current_level_rects = level_rects.get_current_level()
        # Function returns us lists and dict with objects on level
        variables.objects, variables.rects, variables.gems, variables.enemy = load_levels(current_level,
                                                                                          current_level_rects)
    variables.first_level = False


# Calling all buttons in this function so don't call it separately in draw
def menu_draw():
    start_button.draw()
    quit_button.draw()
    sound_button.draw()
    music_button.draw()


# Function to call it in draw
def drawing():
    global menu_active
    # Nothing special, just drawing
    if variables.game_started:
        bground.draw()
        pause_button.draw()
        restart_button.draw()
        for gem in variables.gems.keys():
            gem.draw()
        for obj in variables.objects:
            obj.draw()
            if obj.image == variables.win4 and variables.have_key:
                if player.colliderect(obj):
                    screen.draw.text("YOU WIN ", color="white",
                                     center=(WIDTH/2, HEIGHT/2), fontsize=80)
                    sounds.win.play()
                    clock.schedule(quit, 2.2)
        for en in variables.enemy:
            en.actor.draw()
        player.draw()

        # Updating our player's y
        if variables.is_jumping:
            player.y -= variables.jump_power
            variables.is_jumping = False
            # Playing sound for jumping
            if not variables.is_sound_off:
                sounds.footstep_grass.play()
        # Score of game
        screen.draw.text("Score: " + str(variables.score), color="white", topleft=(10, 10), fontsize=30)
    else:
        screen.clear()
        menu_draw()
        menu_active = False


# Turning off and turning on music
def music_toggle():
    if not music.is_playing('videoplayback.wav'):
        music.play('videoplayback.wav')
    else:
        music.pause()


# Checking some events on mouse down
def on_mouse_down(pos):
    global menu_active, restart_level
    if menu_active:
        if pause_button.collidepoint(pos):
            variables.game_started = False
        elif restart_button.collidepoint(pos):
            restart_level = True
        return

    if start_button.collidepoint(pos):
        start_game()
    elif quit_button.collidepoint(pos):
        quit_game()
    elif sound_button.collidepoint(pos):
        sound_on()
    elif music_button.collidepoint(pos):
        music_toggle()
        music_on()
    menu_active = True


# Chcking events on key down
def on_key_down(key):
    if key == keys.D and variables.game_started:
        variables.walking_right = True
    if key == keys.A and variables.game_started:
        variables.walking_left = True
    if key == keys.W and variables.game_started:
        for rect in variables.rects:
            # Checking can we jump or not
            if player.colliderect(rect) or variables.jump_count <= 2:
                variables.is_jumping = True
                variables.jump_count += 1


# Updating events on key up
def on_key_up(key):
    if key == keys.D and variables.game_started:
        variables.walking_right = False
        player.image = 'player/player_stand'
    if key == keys.A and variables.game_started:
        variables.walking_left = False
        player.image = 'player/player_stand'
    if key == keys.W and variables.game_started:
        variables.is_jumping = False
        player.image = 'player/player_stand'


def update():
    global checkpoint_x, checkpoint_y, restart_level
    first_level()
    # Checking can we go left or not
    if player.left <= 0:
        variables.walking_left = False
    # Checking can we go right or not
    if player.right >= WIDTH:
        variables.walking_right = False

    # Restarting level
    if restart_level:
        cur_lev = levels.get_current_level()
        cur_lev_rect = level_rects.get_current_level()
        variables.objects, variables.rects, variables.gems, variables.enemy = load_levels(cur_lev, cur_lev_rect)
        player.pos = variables.poses[0]
        checkpoint_x, checkpoint_y = variables.poses[0]
        restart_level = False
        variables.score = variables.last_level_score
        variables.jump_power = 70
    for obj in variables.objects:
        # If we are on button we teleport
        if obj.image == variables.teleport:
            if player.colliderect(obj):
                player.pos = 680, 467
        # win, win2, win3 and win4 are actors that tell us we won
        # We checking them seperetly coz winning cases are different
        if obj.image == variables.win3:
            if player.colliderect(obj) and variables.have_key:
                variables.unlocked = True
                variables.have_key = False
        # Checking wins and if door is locked
        if obj.image == variables.win or obj.image == variables.win2 or variables.unlocked:
            if player.colliderect(obj) or variables.unlocked:
                # Switching levels
                levels.switch_level()
                cur_lev = levels.get_current_level()
                level_rects.switch_level()
                cur_lev_rect = level_rects.get_current_level()
                variables.objects, variables.rects, variables.gems, variables.enemy = load_levels(cur_lev, cur_lev_rect)
                player.pos = variables.poses[0]
                checkpoint_x, checkpoint_y = variables.poses[0]
                variables.poses.pop(0)
                variables.unlocked = False
                variables.last_level_score = variables.score

    need_to_be_removed = []
    for en in variables.enemy:
        en.animate()
        # If we have collision with enemy we start again
        if player.colliderect(en.actor):
            player.pos = checkpoint_x, checkpoint_y
    # Checking collison with platforms
    for platform in variables.rects:
        if player.colliderect(platform):
            player.y = platform.top - 20
            variables.jump_count = 0
    # Checking if we fall
    if player.top > HEIGHT:
        player.pos = checkpoint_x, checkpoint_y
    # If we walking right
    if variables.walking_right:
        # getting time so we don't call sound continously
        current_time = time.time()
        if not variables.is_sound_off:
            if current_time - variables.last_footstep_time > variables.footstep_interval:
                sounds.footstep_grass1.play()
                variables.last_footstep_time = current_time
        variables.frame_delay -= 1
        if variables.frame_delay == 0:
            player.x += variables.walk_speed
            # changing images for animation of walking
            variables.current_frame = (variables.current_frame + 1) % len(variables.walking)
            player.image = variables.walking[variables.current_frame]
            variables.frame_delay = 3
    # Same here but for left
    if variables.walking_left:
        current_time = time.time()
        if not variables.is_sound_off:
            if current_time - variables.last_footstep_time > variables.footstep_interval:
                sounds.footstep_grass1.play()
                variables.last_footstep_time = current_time
        variables.frame_delay -= 1
        if variables.frame_delay == 0:
            player.x -= variables.walk_speed
            variables.current_frame = (variables.current_frame + 1) % len(variables.walking)
            player.image = variables.walking[variables.current_frame]
            player.mirror = True
            variables.frame_delay = 3

    # Checking if we are on ground
    if not variables.is_jumping:
        player.y += variables.gravity
        for platform in variables.rects:
            if player.colliderect(platform):
                if player.bottom >= platform.centery:
                    player.y = platform.top - 20
                    variables.jump_count = 1

    # Checking which gem we take
    for gem in variables.gems.keys():
        if player.collidepoint(gem.x, gem.y):
            if variables.gems[gem] == 'Jump':
                jump_boost()
            elif variables.gems[gem] == 'Point':
                variables.score += 10
            elif variables.gems[gem] == 'Lock':
                jump_boost()
                variables.have_key = True
            elif variables.gems[gem] == 'Lock_r':
                variables.have_key = True
            need_to_be_removed.append(gem)
    for rm in need_to_be_removed:
        del variables.gems[rm]
    inactive_boost()


def draw():
    drawing()


pgzrun.go()
