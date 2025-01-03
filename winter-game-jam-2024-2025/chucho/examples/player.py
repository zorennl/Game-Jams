from pyray import *
from os.path import join as os


# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

# PLAYER CLASS
class player:
    def __init__(self, pos: Vector2, spd, size: float, rotation, texture):
        self.pos = pos
        self.spd = spd
        self.size = size
        self.rotation = rotation
        self.texture = texture

    def draw(self):
        # self.tint = Color()
        # load_texture(sef.texture)
        draw_texture_ex(self.texture, self.pos, self.rotation, self.size, WHITE)
        
    def move(self, up: KeyboardKey, down: KeyboardKey, left: KeyboardKey, right: KeyboardKey):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        if is_key_down(up):
            self.pos.y -= self.spd
        if is_key_down(down):
            self.pos.y += self.spd
        if is_key_down(left):
            self.pos.x -= self.spd
        if is_key_down(right):
            self.pos.x += self.spd



testpos = Vector2(400,250)

init_window(WINDOW_WIDTH,WINDOW_HEIGHT,"player")

playertextureraw = os('assets','player.png')
playertexture = load_texture(playertextureraw)

set_target_fps(60)

set_exit_key(KEY_Q)

test = player(testpos,2,2,0,playertexture)

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)

    test.draw()
    test.move(KEY_W,KEY_S,KEY_A,KEY_D)
    
    end_drawing()

close_window()
