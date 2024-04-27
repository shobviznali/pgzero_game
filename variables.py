is_sound_off = False
is_music_off = True
walking_right = False
walking_left = False
game_started = False
is_jumping = False
on_ground = True
first_level = True
last_level_score = 0
jump_power = 70
gravity = 2
walk_speed = 4
current_frame = 0
frame_delay = 3
boost_time = 0
boost_seconds = 3
jump_count = 0
last_footstep_time = 0
footstep_interval = 0.5
objects = []
rects = []
gems = {}
enemy = []
have_key = False
unlocked = False
poses = [[40, 400], [23, 246], [40, 400]]
win = "game_images/other/flagreen_up"
win2 = "game_images/other/flagreen_down"
win3 = "game_images/other/doorgreen_lock.png"
win4 = "game_images/other/door_bottom.png"
teleport = "game_images/other/buttonred.png"

boost_active = False
walking = ['player/player_walk1', 'player/player_walk2', 'player/player_walk3', 'player/player_walk4', 'player/player_walk5']

score = 0


levels = []
levels_rects = []
