from pyray import *
import math as m


init_window(500,500,"chucho")
set_target_fps(60)


playerx = 250
playery = 250

def normAngle(px,py,dist):
    mx = get_mouse_x()
    my = get_mouse_y()
    dx = mx-px; dy = my-py
    if dx == 0:
        if dy > 0:
            dy = dist
        else: dy = -1*dist
    else:
        angle = m.atan(dy/dx)
        dx = int(m.cos(angle)*dist)
        dy = int(m.sin(angle)*dist)
    if mx < px:
        dx *= -1; dy *= -1
    return (dx,dy)






while not window_should_close():
    begin_drawing()
    clear_background(WHITE)

    draw_circle(playerx,playery,10,RED)
    swordx = normAngle(playerx,playery,50)[0]
    swordy = normAngle(playerx,playery,50)[1]
    draw_circle(playerx+swordx,playery+swordy,5,ORANGE)


    end_drawing()
close_window()
