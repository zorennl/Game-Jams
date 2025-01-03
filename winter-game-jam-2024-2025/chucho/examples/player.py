from pyray import *

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

# PLAYER CLASS
class player:
    def __init__(self, pos, spd, size, rotation, texture):
        self.pos = Vector2()
        self.spd = spd
        self.size = float()
        self.rotation = rotation
        self.texture = texture
        # self.tint = Color()
        # load_texture(texture)
        draw_texture_ex(texture, pos, rotation, size, WHITE)
        
    def move(self, up, down, left, right):
        self.up = KeyboardKey
        self.down = KeyboardKey
        self.left = KeyboardKey
        self.right = KeyboardKey
        if is_key_down(up):
            self.pos.y -= self.spd
        if is_key_down(down):
            self.pos.y += self.spd
        if is_key_down(left):
            self.pos.x -= self.spd
        if is_key_down(right):
            self.pos.x += self.spd

playertextureraw = 'assets/player.png'
playertexture = load_texture(playertextureraw)

testpos = Vector2(400,250)

init_window(WINDOW_WIDTH,WINDOW_HEIGHT,"player")

set_target_fps(60)

set_exit_key(KEY_Q)

while not window_should_close():
    begin_drawing()

    test = player(testpos,2,2,0,playertexture)#.move(KEY_W,KEY_S,KEY_A,KEY_D)
    
    end_drawing()

close_window()
