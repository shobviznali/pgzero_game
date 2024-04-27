import variables
from helper import sound_button, music_button
import time


# Starting
def start_game():
    if variables.game_started:
        variables.game_started = False
    else:
        variables.game_started = True
    print("Starting game...", variables.game_started)


# Checking if sound is on
def sound_on():
    if variables.is_sound_off:
        variables.is_sound_off = False
        sound_button.image = 'main_menu/sound_on.png'
    else:
        variables.is_sound_off = True
        sound_button.image = 'main_menu/sound_off.png'


# Quit button
def quit_game():
    exit()


# Checking if music is on
def music_on():
    if variables.is_music_off:
        variables.is_music_off = False
        music_button.image = 'main_menu/music_on'
    else:
        variables.is_music_off = True
        music_button.image = 'main_menu/music_off'


# Giving jump boost
def jump_boost():
    variables.jump_power = 200
    variables.boost_time = time.time()
    variables.score += 50
    variables.boost_active = True


# Inactivating boost
def inactive_boost():
    if variables.boost_active and time.time() >= variables.boost_time + variables.boost_seconds:
        variables.boost_active = False
        variables.jump_power = 70
