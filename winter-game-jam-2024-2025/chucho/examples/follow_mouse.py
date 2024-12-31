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
    draw_text(f"dx: {dx}, dy: {dy}",0,0,20,DARKPURPLE)
    if dx == 0:
        dy = -1*dist
    else: 
        angle = dy/dx
        dx = int(m.cos(m.atan(angle))*dist)
        dy = int(m.sin(m.atan(angle))*dist)
    draw_text(f"angle (rad): {m.atan(angle)}",0,30,20,DARKPURPLE)
    draw_text(f"angle (deg): {m.degrees(m.atan(angle))}",0,60,20,DARKPURPLE)
    if get_mouse_x() < playerx:
        dx *= -1
        dy *= -1

    if get_mouse_x()-playerx == 0:
        if get_mouse_y()-playery > 0:
            dy = dist

    draw_circle(playerx,playery,10,RED)
    draw_rectangle(playerx+dx,playery+dy,10,10,ORANGE)


    end_drawing()
close_window()
