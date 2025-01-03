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
playerspd = 12
playermaxspd = 3

# ENEMY
enemyList = []
class enemy:
    def __init__(self,x,y,spd,type):
        self.x = x
        self.y = y
        self.spd = spd
        self.type = type
    def move(self):
        if self.type == 1:
            self.x += moveTowards(self.x, self.y, player.x, player.y, self.spd)[0]
            self.y += moveTowards(self.x, self.y, player.x, player.y, self.spd)[1]
        if self.type == 2:
            try: self.vx += 0
            except: self.vx = 0

            try: self.vy += 0
            except: self.vy = 0

            randspd = get_random_value(1,10)*.1
            self.vx += moveTowards(self.x, self.y, player.x, player.y, self.spd * randspd)[0]
            self.vy += moveTowards(self.x, self.y, player.x, player.y, self.spd * randspd)[1]
            self.vx *= .8; self.vy *= .8
            self.x += self.vx; self.y += self.vy


box1 = Rectangle(0,0,10,10)
box2 = Rectangle(0,90,10,10)
box3 = Rectangle(90,0,10,10)
box4 = Rectangle(90,90,10,10)


# MOVE TOWARDS
def moveTowards(x1,y1,x2,y2,dist):
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

    # DRAW ENEMY
    enemyNumber = 0
    for item in enemyList:
        draw_rectangle(int(item.x),int(item.y),10,10,GREEN)
        item.move()
        if abs(item.x-weapon.x) < 10:
            if abs(item.y-weapon.y) < 10:
                enemyList.pop(enemyNumber)
        enemyNumber += 1
    
    if is_key_pressed(KEY_ONE):
        spawn = get_random_value(1,200)
        enemyList.append(enemy(int(m.sin(spawn)),int(m.cos(spawn)),3,1))
    if is_key_pressed(KEY_TWO):
        spawn = get_random_value(1,200)
        enemyList.append(enemy(int(m.sin(spawn)),int(m.cos(spawn)),2,2))
       
    # DRAW WEAPON
    weaponPos = Vector2(moveTowards(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, get_mouse_x(), get_mouse_y(), 30)[0],
                        moveTowards(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, get_mouse_x(), get_mouse_y(), 30)[1])
    weapon = vector2_add(weaponPos, camera.target)
    draw_circle_v(weapon,5,ORANGE)
    
    
    # POSITION MARKERS
    draw_rectangle_rec(box1, RED)
    draw_rectangle_rec(box2, RED)
    draw_rectangle_rec(box3, RED)
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
