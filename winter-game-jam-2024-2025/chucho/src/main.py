from pyray import *
from os.path import join as os
import math as m
# CONSTANTS
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

# VARIABLES
oldx = 0
oldy = 0
newx = 0
newy = 0

# SAVE
open('saves\\save', 'a')

read = open('saves\\save', 'r')

readlist = read.readlines()

if readlist: 
    savex = float(readlist[0])
    savey = float(readlist[1])
else:
    savex = 45
    savey = 45

# RAW SPRITES
raw_bkg = os('assets', 'bkg.png')

# PLAYER 
player = Rectangle(savex, savey, 10, 10)
playerspd = 1
playermaxspd = 3

# ENEMY
box1 = Rectangle(0,0,10,10)
drawbox1 = True
box2 = Rectangle(0,90,10,10)
drawbox2 = True
box3 = Rectangle(90,0,10,10)
drawbox3 = True
box4 = Rectangle(90,90,10,10)
drawbox4 = True

# WEAPON TO MOUSE
def normAngle(x1,y1,x2,y2,dist):
    dx = x2-x1; dy = y2-y1
    if dx == 0:
        if dy > 0:
            dy = dist
        else: dy = -1*dist
    else:
        angle = m.atan(dy/dx)
        dx = int(m.cos(angle)*dist)
        dy = int(m.sin(angle)*dist)
    if x2 < x1:
        dx *= -1; dy *= -1
    return (dx,dy)

# DEFINE CAMERA
camera = Camera2D()
camera.zoom = 1

# DEBUG TOGGLE
dbtoggle = False

set_config_flags(FLAG_WINDOW_UNDECORATED)
init_window(WINDOW_WIDTH,WINDOW_HEIGHT,"chucho")
set_target_fps(60)

# LOAD TEXTURES
# bkg = load_texture(raw_bkg)

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
    if playerspd < playermaxspd and playerspd > -playermaxspd:
        if spdx or spdy > 0 and playerspd < 5:
            playerspd += .03
        if spdx or spdy < 0 and playerspd > -5:
            playerspd += .03
    if spdx == 0 and spdy == 0:
        playerspd = 1
    # CAMERA
    camera.target = Vector2(player.x + player.width / 2, player.y + player.height / 2)
    camera.offset = Vector2(WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2)
    
    # DRAWING
    begin_drawing()
    clear_background(BLACK)
        
    begin_mode_2d(camera)
    
    # DRAW PLAYER
    draw_rectangle_rec(player, WHITE)
       
    # DRAW WEAPON
    weaponPos = Vector2(normAngle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, get_mouse_x(), get_mouse_y(), 30)[0],
                        normAngle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, get_mouse_x(), get_mouse_y(), 30)[1])
    weapon = vector2_add(weaponPos, camera.target)
    draw_circle_v(weapon,5,ORANGE)
    
    collisionbox1 = check_collision_circle_rec(weapon, 5, box1)

    if collisionbox1 == True:
        drawbox1 = False

    collisionbox2 = check_collision_circle_rec(weapon, 5, box2)

    if collisionbox2 == True:
        drawbox2 = False

    collisionbox3 = check_collision_circle_rec(weapon, 5, box3)

    if collisionbox3 == True:
        drawbox3 = False

    collisionbox4 = check_collision_circle_rec(weapon, 5, box4)

    if collisionbox4 == True:
        drawbox4 = False
    
    # POSITION MARKERS
    if drawbox1 == True:
        draw_rectangle_rec(box1, RED)
    if drawbox2 == True:
        draw_rectangle_rec(box2, RED)
    if drawbox3 == True:
        draw_rectangle_rec(box3, RED)
    if drawbox4 == True:
        draw_rectangle_rec(box4, RED)
    end_mode_2d()
    
    # DEBUG
    if is_key_pressed(KEY_F3):
        dbtoggle = not dbtoggle

    if dbtoggle == True:
        draw_text(f'pos: {round(player.x,2,), round(player.y,2)}\nspd: {round(spdx, 2), round(spdy,2)}\nfps: {get_fps()}', 0, 0, 2, RAYWHITE)
        
    # SPEED CALC
    oldx = newx; oldy = newy
    
    end_drawing()
close_window()
save = open('saves/save', 'w')
save.write(f'{player.x}\n{player.y}')
