from pyray import *
import math as m


init_window(1000,1000,"chucho")
set_target_fps(60)

dist = 50

playerx = 500
playery = 500

while not window_should_close():
    begin_drawing()
    clear_background(WHITE)

    dx = get_mouse_x()-playerx
    dy = get_mouse_y()-playery

    if dx == 0:
        angle = m.pi
    else: angle = dy/dx

    dx = int(m.cos(m.atan(angle))*dist)
    dy = int(m.sin(m.atan(angle))*dist)

    if get_mouse_x() < playerx:
        dx *= -1
        dy *= -1

    draw_circle(playerx,playery,10,RED)
    draw_rectangle(playerx+dx,playery+dy,10,10,ORANGE)


    end_drawing()
close_window()
