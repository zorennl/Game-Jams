from pyray import *

# CONSTANTS
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100

# VARIABLES
oldx = 0
oldy = 0
newx = 0
newy = 0

# PLAYER 
player = Rectangle(45, 45, 10, 10)
playerspd = 2

# DEFINE CAMERA
camera = Camera2D()
camera.zoom = 1

# DEBUG TOGGLE
dbtoggle = False

set_config_flags(FLAG_WINDOW_UNDECORATED)
init_window(WINDOW_WIDTH,WINDOW_HEIGHT,"chucho")
set_target_fps(60)

while not window_should_close():

    # SPEED CALCULATION
    fps = get_fps()
    newx = player.x
    newy = player.y
    spdx = (oldx - newx)
    spdy = (oldy - newy)
    
    # MOVEMENT
    if is_key_down(KEY_W):
        player.y -= playerspd
    if is_key_down(KEY_A):
        player.x -= playerspd
    if is_key_down(KEY_S):
        player.y += playerspd
    if is_key_down(KEY_D):
        player.x += playerspd

    # CAMERA
    camera.target = Vector2(player.x - 45, player.y - 45)
    
    # DRAWING
    begin_drawing()
    clear_background(BLACK)
    
    begin_mode_2d(camera)
    
    draw_rectangle_rec(player, WHITE)

    # POSITION MARKERS
    draw_rectangle(0, 0, 10, 10, RED)
    draw_rectangle(90, 0, 10, 10, RED)
    draw_rectangle(90, 90, 10, 10, RED)
    draw_rectangle(0, 90, 10, 10, RED)
        
    end_mode_2d()
    
    # DEBUG
    if is_key_pressed(KEY_F3):
        dbtoggle = not dbtoggle

    if dbtoggle == True:
        draw_text(f'px: {player.x}, py: {player.y}\n spd: {spdx, spdy}', 0, 0, 2, WHITE)
        
    # SPEED CALC
    oldx = newx; oldy = newy
      
    end_drawing()
close_window()
