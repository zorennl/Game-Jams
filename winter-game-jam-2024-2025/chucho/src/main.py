import math
import os as pyos  # Renamed to 'pyos' to avoid confusion with 'os' function usage
from pyray import *

################################################################################
# GLOBAL CONSTANTS & INITIALIZATION
################################################################################

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

SAVE_FOLDER = "saves"
SAVE_FILE   = pyos.path.join(SAVE_FOLDER, "save")

# Ensure the "saves" directory exists
pyos.makedirs(SAVE_FOLDER, exist_ok=True)

################################################################################
# CLASSES
################################################################################

class Enemy:
    """
    Simple enemy class that either chases the player directly (type=1)
    or does a pseudo-chase with drifting velocity (type=2).
    """
    def __init__(self, x, y, speed, enemy_type):
        self.x = float(x)
        self.y = float(y)
        self.spd = float(speed)
        self.type = enemy_type
        # For type=2, store some velocity components:
        self.vx = 0.0
        self.vy = 0.0

    def move(self, player_rect):
        """
        Move the enemy towards the player's position, 
        with behavior depending on `self.type`.
        """
        px, py = player_rect.x, player_rect.y

        if self.type == 1:
            # Direct chase
            dx, dy = move_towards(self.x, self.y, px, py, self.spd)
            self.x += dx
            self.y += dy

        elif self.type == 2:
            # Drifting chase
            rand_spd_scale = get_random_value(1, 10) * 0.1  # from 0.1 to 1.0
            dx, dy = move_towards(self.x, self.y, px, py, self.spd * rand_spd_scale)

            # Increase velocity, then dampen
            self.vx += dx
            self.vy += dy
            self.vx *= 0.8
            self.vy *= 0.8

            self.x += self.vx
            self.y += self.vy


################################################################################
# UTILITY FUNCTIONS
################################################################################

def move_towards(x1, y1, x2, y2, dist):
    """
    Returns a (dx, dy) that moves point (x1,y1) by 'dist' units toward (x2,y2).
    """
    dx = x2 - x1
    dy = y2 - y1

    # Avoid division by zero if dx=0
    if abs(dx) < 1e-6:
        # purely vertical
        dy_sign = 1 if dy >= 0 else -1
        return 0, dy_sign * dist
    else:
        angle = math.atan2(dy, dx)  # Use atan2 for safer angle handling
        return (math.cos(angle) * dist, math.sin(angle) * dist)


def vector2_add(vec2_a, vec2_b):
    """
    Adds two Vector2 objects or (x, y) tuples.
    """
    # In pyray, a Vector2 can be manipulated just like a tuple.
    return Vector2(vec2_a.x + vec2_b.x, vec2_a.y + vec2_b.y)


def clamp(value, minimum, maximum):
    """
    Clamps a numeric value between [minimum, maximum].
    """
    return max(minimum, min(value, maximum))


################################################################################
# MAIN GAME LOGIC
################################################################################

def main():
    ############################################################################
    # INITIAL SETUP
    ############################################################################

    # Attempt to load last saved position
    player_start_x, player_start_y = 45.0, 45.0

    try:
        with open(SAVE_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                player_start_x = float(lines[0].strip())
                player_start_y = float(lines[1].strip())
    except FileNotFoundError:
        # No prior save
        pass

    # Create the player rectangle
    player = Rectangle(player_start_x, player_start_y, 10, 10)

    # Speed variables
    # Using an initial speed and max speed
    base_move_speed  = 2.0  # base speed per frame
    max_move_speed   = 5.0
    speed_multiplier = 1.0  # Will ramp up if the player is continuously moving
    # If you want to incorporate time-based movement, use dt in the loop below

    # Initialize enemies
    enemy_list = []

    # Simple markers
    box1 = Rectangle(0,   0,   10, 10)
    box2 = Rectangle(0,   90,  10, 10)
    box3 = Rectangle(90,  0,   10, 10)
    box4 = Rectangle(90,  90,  10, 10)

    # Define a camera
    camera = Camera2D()
    camera.zoom = 1.0

    # Debug toggle
    dbtoggle = False

    # Create window
    set_config_flags(FLAG_WINDOW_UNDECORATED)
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "ChuchoGame")
    set_target_fps(60)

    # Main loop
    old_player_x = player.x
    old_player_y = player.y

    while not window_should_close():

        # OPTION A) Time-based movement (uncomment if you want to use dt)
        # dt = get_frame_time()

        ########################################################################
        # INPUT HANDLING
        ########################################################################

        # Basic WASD movement
        # If using dt: step = base_move_speed * speed_multiplier * dt
        step = base_move_speed * speed_multiplier
        if is_key_down(KEY_W):
            player.y -= step
        if is_key_down(KEY_A):
            player.x -= step
        if is_key_down(KEY_S):
            player.y += step
        if is_key_down(KEY_D):
            player.x += step

        # Increase or reset speed_multiplier based on movement
        # (keeps accelerating while moving; reset if no input)
        spdx = player.x - old_player_x
        spdy = player.y - old_player_y
        moving_horizontally = abs(spdx) > 0.01
        moving_vertically   = abs(spdy) > 0.01

        if moving_horizontally or moving_vertically:
            speed_multiplier += 0.02
        else:
            speed_multiplier = 1.0

        # clamp speed_multiplier
        speed_multiplier = clamp(speed_multiplier, 1.0, max_move_speed)

        # Toggle debug
        if is_key_pressed(KEY_F3):
            dbtoggle = not dbtoggle

        # Spawn enemies with keys 1 or 2
        if is_key_pressed(KEY_ONE):
            spawn = get_random_value(0, 1000) / 1000.0 * math.tau  # random angle
            ex = math.sin(spawn) * 200
            ey = math.cos(spawn) * 200
            enemy_list.append(Enemy(ex, ey, 3, 1))

        if is_key_pressed(KEY_TWO):
            spawn = get_random_value(0, 1000) / 1000.0 * math.tau
            ex = math.sin(spawn) * 200
            ey = math.cos(spawn) * 200
            enemy_list.append(Enemy(ex, ey, 2, 2))

        ########################################################################
        # CAMERA LOGIC
        ########################################################################

        camera.target = Vector2(player.x + player.width / 2.0,
                                player.y + player.height / 2.0)
        camera.offset = Vector2(WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0)

        ########################################################################
        # DRAW
        ########################################################################

        begin_drawing()
        clear_background(BLACK)

        begin_mode_2d(camera)

        # Player
        draw_rectangle_rec(player, WHITE)

        # Enemies
        # Also handle collision with "weapon"
        # We'll compute 'weapon' below
        weapon_radius = 5
        # weapon is based on "moveTowards" from screen center to mouse
        # but we have to consider the camera offset
        screen_center_x = WINDOW_WIDTH / 2
        screen_center_y = WINDOW_HEIGHT / 2

        # local mouse coords relative to screen center
        local_dx, local_dy = move_towards(
            screen_center_x,
            screen_center_y,
            get_mouse_x(),
            get_mouse_y(),
            30
        )
        # weapon local to camera
        # Then we add camera.target to shift it into world coords
        weapon_x = camera.target.x + local_dx - screen_center_x
        weapon_y = camera.target.y + local_dy - screen_center_y

        # Update & draw enemies
        for i, e in reversed(list(enumerate(enemy_list))):
            draw_rectangle(int(e.x), int(e.y), 10, 10, GREEN)
            e.move(player)

            # check collision with weapon
            if abs(e.x - weapon_x) < 10 and abs(e.y - weapon_y) < 10:
                # remove enemy
                enemy_list.pop(i)

        # Draw weapon
        draw_circle(int(weapon_x), int(weapon_y), weapon_radius, ORANGE)

        # Position markers
        draw_rectangle_rec(box1, RED)
        draw_rectangle_rec(box2, RED)
        draw_rectangle_rec(box3, RED)
        draw_rectangle_rec(box4, RED)

        end_mode_2d()

        ########################################################################
        # DEBUG INFO
        ########################################################################

        if dbtoggle:
            text_lines = [
                f"pos: ({round(player.x,2)}, {round(player.y,2)})",
                f"spd: ({round(spdx,2)}, {round(spdy,2)})",
                f"speed_mult: {round(speed_multiplier, 2)}",
                f"fps: {get_fps()}"
            ]
            # Draw small text at top left
            for idx, line in enumerate(text_lines):
                draw_text(line, 2, 2 + idx * 10, 10, RAYWHITE)

        ########################################################################
        # END FRAME
        ########################################################################

        old_player_x = player.x
        old_player_y = player.y

        end_drawing()

    # On exit, save the player's location
    with open(SAVE_FILE, 'w') as save:
        save.write(f"{player.x}\n{player.y}\n")

    close_window()

################################################################################
# ENTRY POINT
################################################################################

if __name__ == "__main__":
    main()
