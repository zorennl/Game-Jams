from pyray import *
import math as m

class enemy:
    def __init__(self,x,y,spd,type):
        self.x = x
        self.y = y
        self.spd = spd
        self.type = type
    def move(self):
        if self.type == 1:
            self.x += normAngle(self.x,self.y,get_mouse_x(),get_mouse_y(),self.spd)[0]
            self.y += normAngle(self.x,self.y,get_mouse_x(),get_mouse_y(),self.spd)[1]
        if self.type == 2:
            try: self.vx += 0
            except: self.vx = 0

            try: self.vy += 0
            except: self.vy = 0

            randspd = get_random_value(1,10)*.1
            self.vx += normAngle(self.x,self.y,get_mouse_x(),get_mouse_y(),self.spd*randspd)[0]
            self.vy += normAngle(self.x,self.y,get_mouse_x(),get_mouse_y(),self.spd*randspd)[1]
            self.vx *= .8; self.vy *= .8
            self.x += self.vx; self.y += self.vy



def normAngle(px,py,twx,twy,dist):
    dx = twx-px; dy = twy-py
    if dx == 0:
        if dy > 0:
            dy = dist
        else: dy = -1*dist
    else:
        angle = m.atan(dy/dx)
        dx = m.cos(angle)*dist
        dy = m.sin(angle)*dist
    if twx < px:
        dx *= -1; dy *= -1
    return dx, dy




init_window(500,500,"enemy")
set_target_fps(60)

enemyList = []


while not window_should_close():
    begin_drawing()
    clear_background(WHITE)

    if is_key_pressed(KEY_ONE):
        enemyList.append(enemy(0,0,2,1))
    if is_key_pressed(KEY_TWO):
        enemyList.append(enemy(0,0,2,2))

    i = 0
    for item in enemyList:

        draw_rectangle(int(item.x),int(item.y),20,20,RED)
        item.move()
        if abs(item.x-get_mouse_x()) < 10:
            if abs(item.y-get_mouse_y()) < 10:
                enemyList.pop(i)
        i += 1


    end_drawing()
close_window()