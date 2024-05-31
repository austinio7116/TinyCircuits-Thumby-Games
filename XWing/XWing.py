import thumby
import math
import random
import time
from thumbyAudio import audio

# Initialize the screen
thumby.display.setFPS(30)
random.seed(time.ticks_ms())
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

# Define screen dimensions
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40

# BITMAP: width: 72, height: 40
cockpit = bytearray([0,0,0,0,0,0,128,64,32,16,8,4,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,8,16,32,64,128,0,0,0,0,0,0,
           224,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4,8,16,224,
           255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,40,16,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
           255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
           255,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,240,8,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,240,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,255])
           
# BITMAP: width: 72, height: 40
shop = bytearray([255,255,3,59,75,139,75,59,3,3,255,255,3,251,203,171,147,235,3,3,255,255,3,3,171,3,3,171,3,3,255,255,3,139,83,35,139,83,35,3,255,255,3,19,19,19,163,99,99,19,3,11,11,11,11,251,11,11,11,11,11,99,51,51,83,147,19,3,3,3,255,255,
           255,255,30,30,18,210,210,18,30,30,255,255,30,30,210,210,82,82,94,30,255,255,30,30,210,210,210,210,30,30,255,255,30,222,82,82,82,210,30,30,255,255,0,0,0,63,0,0,2,14,20,20,8,0,0,241,224,0,0,8,20,20,14,2,0,0,31,0,0,0,255,255,
           255,255,240,240,148,151,151,148,240,240,255,255,240,240,151,151,148,148,244,240,255,255,240,240,151,148,144,151,244,240,255,255,240,240,144,149,145,145,240,240,255,255,0,8,14,7,1,193,128,24,48,64,120,192,121,1,121,193,8,120,32,48,24,128,193,7,15,8,0,0,255,255,
           255,255,128,136,174,170,186,136,128,148,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,255,255,128,128,128,128,128,128,129,131,136,144,146,147,144,144,144,147,146,144,136,128,131,129,128,128,128,128,128,128,255,255,
           255,255,128,190,170,170,128,168,144,168,128,186,128,190,168,128,128,128,128,128,255,128,174,170,170,186,128,190,136,190,128,190,162,162,190,128,190,138,142,128,255,255,128,136,174,170,186,136,128,148,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,255,255])
           
# Define 3D projection and transformation functions
def project(x, y, z, screen_width, screen_height, fov, viewer_distance):
    if viewer_distance + z == 0:
        z = z + .0001  # Prevent division by zero
    factor = fov / (viewer_distance + z)
    x_proj = x * factor + screen_width / 2
    y_proj = -y * factor + screen_height / 2
    return int(x_proj), int(y_proj)

def rotate_x(x, y, z, angle):
    rad = math.radians(angle)
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y, z = y * cosa - z * sina, y * sina + z * cosa
    return x, y, z

def rotate_y(x, y, z, angle):
    rad = math.radians(angle)
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x, z = x * cosa + z * sina, -x * sina + z * cosa
    return x, y, z

def rotate_z(x, y, z, angle):
    
    rad = math.radians(angle)
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x, y = x * cosa - y * sina, x * sina + y * cosa
    return x, y, z
    
def draw_circle(x_center, y_center, radius, c):
    x = radius
    y = 0
    decision = 1 - x

    while y <= x:
        thumby.display.setPixel(int(x_center + x), int(y_center + y), c)
        thumby.display.setPixel(int(x_center - x), int(y_center + y), c)
        thumby.display.setPixel(int(x_center + x), int(y_center - y), c)
        thumby.display.setPixel(int(x_center - x), int(y_center - y), c)
        thumby.display.setPixel(int(x_center + y), int(y_center + x), c)
        thumby.display.setPixel(int(x_center - y), int(y_center + x), c)
        thumby.display.setPixel(int(x_center + y), int(y_center - x), c)
        thumby.display.setPixel(int(x_center - y), int(y_center - x), c)

        y += 1
        if decision <= 0:
            decision += 2 * y + 1
        else:
            x -= 1
            decision += 2 * (y - x) + 1

# Initialize global variables
stars = []
planets = []
ships = []  # List to store enemy ships
enemy_lasers = []  # List to store enemy lasers
player_lasers = []  # List to store player lasers
hit_effects = []  # List to store hit effects

def reset_level_variables():
    global ships, stars, planets, rotation_x, rotation_y, rotation_z
    global player_lasers, enemy_lasers, hit_effects

    # Reset variables
    ships = []
    stars = [(random.randint(-50, 50), random.randint(-30, 30), random.randint(10, 50)) for _ in range(100)]
    planets = [(random.randint(-50, 50), random.randint(-30, 30), random.randint(40, 100)) for _ in range(random.randint(1, 4))]
    rotation_x, rotation_y, rotation_z = 0, 0, 0
    player_lasers = []
    enemy_lasers = []
    hit_effects = []
    

kill_count = 0
score = 0
money = 0

# Game state variables
levels = [
    {"intro": "Level 1: Hey rookie - Defend the rebel base.  Make sure no more than 5 ships get by.", "max_passed": 5},
    {"intro": "Level 2: Here comes another wave - we can't take much more damage!", "max_passed": 3},
    {"intro": "Level 3: This is the final push - just hold them off a little longer", "max_passed": 1},
]

shop_items = [
    {"name": "Heart", "cost": 10, "effect": "shield"},
    {"name": "Chip", "cost": 20, "effect": "rotation_speed"},
    {"name": "A", "cost": 30, "effect": "rate_of_fire"},
    {"name": "Shield", "cost": 40, "effect": "laser_speed"},
    {"name": "Missile", "cost": 50, "effect": "smart_bomb"},
    {"name": "Lasers", "cost": 60, "effect": "extra_lasers"},
    {"name": "Music", "cost": 70, "effect": "play_music"},
    {"name": "Shot", "cost": 80, "effect": "hard_mode"},
]

sequence = [
    (294, 100), (294, 100), (294, 100),  # Triplet of D
    (392, 600), (587, 600),                  # G, D
    (523, 100), (494, 100), (440, 100),     # Triplet C, B, A
    (784, 600), (587, 300),                  # G (octave up), D
    (523, 100), (494, 100), (440, 100),     # Triplet C, B, A
    (784, 600), (587, 300),                   # G (octave up), D
    (523, 100), (494, 100), (523, 100),
    (440, 600)
]

no_money_sequence = [(2000, 100), (1000, 100), (1500, 100), (1000, 100), (1250, 100), (1000, 200)]

buy_sequence = [(1000, 100),(1250, 100)]

def play_audio_sequence(sequence):
    # This function plays a sequence of audio tones.
    # It iterates over the provided sequence of (frequency, duration) tuples and plays each tone using the audio library.
    for freq, duration in sequence:
        audio.playBlocking(freq, duration)

current_price = 0
current_level = 0
ships_passed = 0
last_shot_time = 0

# Player stats
player_stats = {
    "time_between_shots": 1000,
    "rotation_speed": 3.0,
    "laser_speed": 3,
    "shield": 0,
    "smart_bombs": 0,
    "extra_lasers": 0,
    "hard_mode":0,
}

def storyteller(text, start_x, start_y, area_width, area_height, font_width, font_height):
    """Display the given text with a typewriter effect."""
    letter_length, line_height_change = font_width + 1, font_height + 1
    scroll_speed, max_lines = 0.05, (area_height - font_height) // line_height_change
    letter_position, line_height, lines_printed = start_x, start_y, 0
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.fill(0)

    words = text.split()
    for word in words:
        if letter_position + len(word) * letter_length >= start_x + area_width:
            line_height += line_height_change
            letter_position = start_x
            lines_printed += 1

        if lines_printed >= max_lines:
            while True:
                thumby.display.drawText("...", start_x, start_y + area_height - font_height, 1)
                thumby.display.update()
                if thumby.buttonA.justPressed():
                    break
                time.sleep(0.1)
                thumby.display.drawFilledRectangle(start_x, start_y + area_height - font_height, area_width, font_height, 0)
                thumby.display.update()
                if thumby.buttonA.justPressed():
                    break
                time.sleep(0.1)
            thumby.display.fill(0)
            letter_position, line_height, lines_printed = start_x, start_y, 0

        for i in word:
            thumby.display.drawText(i, letter_position, line_height, 1)
            thumby.display.update()
            letter_position += letter_length
            time.sleep(scroll_speed)
            thumby.audio.play(random.randrange(270, 300), 50)

        letter_position += letter_length  # Add a space between words

    thumby.audio.play(300, 100)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

def show_intro_screen(text):
    storyteller(text,0,0,72,40,5,7)
    thumby.display.update()
    time.sleep(1)

flashon=1
# Function to render the shop screen
def render_shop_screen(selected_option, total_gold):
    global flashon, current_price
    thumby.display.fill(0)
    thumby.display.blit(shop, 0, 0, 72, 40, 0, 0, 0)
    thumby.display.drawText(str(total_gold), 52, 33, 1)
    
    # Display the cost of the selected item
    if selected_option < 8:
        current_price = shop_items[selected_option]["cost"]
    thumby.display.drawText(str(current_price), 12, 25, 1)
    
    # Highlight the selected option
    highlight_positions = [
        (4, 10), (14, 10), (24, 10), (34, 10),  # Top row
        (4, 21), (14, 21), (24, 21), (34, 21),  # Bottom row
        (17, 34)                      # Exit and Buy buttons
    ]
    x, y = highlight_positions[selected_option]
    flashon = (flashon + 1) % 2
    if selected_option in [8, 9]:
        thumby.display.drawLine(x, y, x, y+2, flashon)
        thumby.display.drawLine(x-1, y, x-1, y+2, flashon)
        thumby.display.drawLine(x+1, y, x+1, y+2, flashon)
    else:
        thumby.display.drawLine(x, y, x + 3, y, flashon)
        thumby.display.drawLine(x, y+1, x + 3, y+1, flashon)
    
    thumby.display.update()

# Function to handle shop input
def shop_input(selected_option):
    if thumby.buttonU.justPressed():
        if selected_option >= 4 and selected_option <= 7:
            selected_option -= 4
        elif selected_option >= 8:  # If currently on Exit or Buy button
            selected_option -= 4  # Move to the second row of shop items
    if thumby.buttonD.justPressed():
        if selected_option < 4:
            selected_option += 4
        elif selected_option >= 4 and selected_option <= 7:
            selected_option = 8
    if thumby.buttonL.justPressed():
        if selected_option % 4 > 0 and selected_option != 8:
            selected_option -= 1
    if thumby.buttonR.justPressed():
        if selected_option % 4 < 3 and selected_option != 8:
            selected_option += 1
    if thumby.buttonA.justPressed():
        if selected_option == 8:
            return 'exit'  # Exit button action
        else:
            global current_price
            return 'buy'
    return selected_option


# Function to apply item effects
def apply_item_effect(effect):
    if effect == "shield":
        player_stats["shield"] += 1
    elif effect == "rotation_speed":
        player_stats["rotation_speed"] += 1
    elif effect == "rate_of_fire":
        player_stats["time_between_shots"] *= 0.8
    elif effect == "laser_speed":
        player_stats["laser_speed"] += 1
    elif effect == "play_music":
        play_audio_sequence(sequence)
    elif effect == "smart_bomb":  
        player_stats["smart_bombs"] += 1
    elif effect == "extra_lasers":  
        player_stats["extra_lasers"] += 1
    elif effect == "hard_mode":  
        player_stats["hard_mode"] += 1
        

# Function to display the shop screen
def show_shop_screen(earned_money):
    global money
    money += earned_money
    selected_option = 0
    while True:
        result = shop_input(selected_option)
        if result == 'exit':
            break  # Exit the shop
        elif result == 'buy':
            if money >= current_price:
                money -= current_price
                effect = shop_items[selected_option]["effect"]
                if effect:
                    play_audio_sequence(buy_sequence)
                    apply_item_effect(effect)
            else:
                play_audio_sequence(no_money_sequence)
        else:
            selected_option = result
            
        render_shop_screen(selected_option, money)
        time.sleep(0.2)  # Add a small delay to make the flashing visible

def show_game_over_screen():
    storyteller('Too many ships got through - the rebel base is destroyed.',0,0,72,40,5,7)
    time.sleep(1)
    
def you_win_screen():
    storyteller('The rebel base is secured! Well Done!',0,0,72,40,5,7)
    time.sleep(1)

def spawn_ship():
    x = random.randint(-25, 25)
    y = random.randint(-15, 15)
    z = 50  # Start far away
    ships.append((x, y, z))

# Render stars
def draw_stars(rotation_x, rotation_y, rotation_z):
    for star in stars:
        x, y, z = star
        x, y, z = rotate_x(x, y, z, rotation_x)
        x, y, z = rotate_y(x, y, z, rotation_y)
        x, y, z = rotate_z(x, y, z, rotation_z)
        screen_x, screen_y = project(x, y, z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            thumby.display.setPixel(screen_x, screen_y, 1)

# Render planets
def draw_planets(rotation_x, rotation_y, rotation_z):
    for planet in planets:
        x, y, z = planet
        x, y, z = rotate_x(x, y, z, rotation_x)
        x, y, z = rotate_y(x, y, z, rotation_y)
        x, y, z = rotate_z(x, y, z, rotation_z)
        screen_x, screen_y = project(x, y, z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        size_factor = 50 / (z + 1)
        size = max(2, int(size_factor * 5))  # Planets should be larger than stars
        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            draw_circle(screen_x, screen_y, size, 1)

# Render ships
def draw_x_ships(rotation_x, rotation_y, rotation_z):
    for ship in ships:
        x, y, z = ship
        x, y, z = rotate_x(x, y, z, rotation_x)
        x, y, z = rotate_y(x, y, z, rotation_y)
        x, y, z = rotate_z(x, y, z, rotation_z)
        screen_x, screen_y = project(x, y, z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        size_factor = 50 / (z + 1)
        size = max(1, int(size_factor * 2))
        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            # Draw ship as an "X" that grows larger as it approaches
            thumby.display.drawLine(screen_x - size, screen_y - size, screen_x + size, screen_y + size, 1)
            thumby.display.drawLine(screen_x - size, screen_y + size, screen_x + size, screen_y - size, 1)
            
def draw_ships(rotation_x, rotation_y, rotation_z):
    for ship in ships:
        x, y, z = ship
        x, y, z = rotate_x(x, y, z, rotation_x)
        x, y, z = rotate_y(x, y, z, rotation_y)
        x, y, z = rotate_z(x, y, z, rotation_z)
        screen_x, screen_y = project(x, y, z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        size_factor = 50 / (z + 1)
        size = max(1, int(size_factor * 2))
        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            # Draw ship body as a circle
            draw_circle(screen_x, screen_y, max(1, int(size // 2)), 1)

            # Draw wings and additional lines
            wing_span = size  # Adjust this value as needed for wing size
            wing_length = wing_span // 2

            # Horizontal line connecting wings, starting from the outside of the circle
            thumby.display.drawLine(screen_x - wing_length, screen_y, screen_x - wing_length - wing_span, screen_y, 1)
            thumby.display.drawLine(screen_x + wing_length, screen_y, screen_x + wing_length + wing_span, screen_y, 1)


            # Left wing lines
            thumby.display.drawLine(screen_x - size, screen_y - 2 * wing_length, screen_x - size - wing_length, screen_y - wing_length, 1)  # \
            thumby.display.drawLine(screen_x - size, screen_y + 2 * wing_length, screen_x - size - wing_length, screen_y + wing_length, 1)  # /
            thumby.display.drawLine(screen_x - size - wing_length, screen_y - wing_length, screen_x - size - wing_length, screen_y + wing_length, 1)  # |

            # Right wing lines
            thumby.display.drawLine(screen_x + size, screen_y - 2 * wing_length, screen_x + size + wing_length, screen_y - wing_length, 1)  # /
            thumby.display.drawLine(screen_x + size, screen_y + 2 * wing_length, screen_x + size + wing_length, screen_y + wing_length, 1)  # \
            thumby.display.drawLine(screen_x + size + wing_length, screen_y - wing_length, screen_x + size + wing_length, screen_y + wing_length, 1)  # |


# Render lasers
def draw_lasers(rotation_x, rotation_y, rotation_z, lasers):
    for laser in lasers:
        x, y, z, vx, vy, vz = laser

        # Rotate start point
        rotated_x, rotated_y, rotated_z = rotate_x(x, y, z, rotation_x)
        rotated_x, rotated_y, rotated_z = rotate_y(rotated_x, rotated_y, rotated_z, rotation_y)
        rotated_x, rotated_y, rotated_z = rotate_z(rotated_x, rotated_y, rotated_z, rotation_z)

        #
        rotated_vx, rotated_vy, rotated_vz = rotate_x(vx, vy, vz, rotation_x)
        rotated_vx, rotated_vy, rotated_vz = rotate_y(rotated_vx, rotated_vy, rotated_vz, rotation_y)
        rotated_vx, rotated_vy, rotated_vz = rotate_z(rotated_vx, rotated_vy, rotated_vz, rotation_z)

        # Calculate rotated end point
        rotated_end_x = rotated_x + rotated_vx
        rotated_end_y = rotated_y + rotated_vy
        rotated_end_z = rotated_z + rotated_vz

        # Project start and end points to 2D screen coordinates
        screen_x, screen_y = project(rotated_x, rotated_y, rotated_z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        end_screen_x, end_screen_y = project(rotated_end_x, rotated_end_y, rotated_end_z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)

        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            thumby.display.drawLine(screen_x, screen_y, end_screen_x, end_screen_y, 1)

# Render hit effects
def draw_hit_effects(rotation_x, rotation_y, rotation_z):
    for effect in hit_effects:
        x, y, z, start_time = effect
        x, y, z = rotate_x(x, y, z, rotation_x)
        x, y, z = rotate_y(x, y, z, rotation_y)
        x, y, z = rotate_z(x, y, z, rotation_z)
        screen_x, screen_y = project(x, y, z, SCREEN_WIDTH, SCREEN_HEIGHT, 60, 1)
        size_factor = 50 / (z + 1)
        
        # Generate a random number of circles for the effect
        num_circles = random.randint(3, 7)
        
        for _ in range(num_circles):
            audio.play(100, 10)
            # Generate random offset around the impact point
            offset_x = random.uniform(-4, 4)
            offset_y = random.uniform(-4, 4)
            
            # Generate random size for the circle, scaled by size factor
            radius = max(1, int(size_factor * random.uniform(1, 3)))
            
            # Calculate the position for the circle
            circle_x = screen_x + offset_x
            circle_y = screen_y + offset_y
            
            # Ensure the circle is within screen bounds
            if 0 <= circle_x < SCREEN_WIDTH and 0 <= circle_y < SCREEN_HEIGHT:
                draw_circle(int(circle_x), int(circle_y), radius, 1)

# Handle input and update rotation
rotation_x, rotation_y, rotation_z = 0, 0, 0

# Function to activate smart bomb
def activate_smart_bomb():
    global ships, enemy_lasers, player_stats

    if player_stats["smart_bombs"] > 0:
        player_stats["smart_bombs"] -= 1

        # Flash the screen white
        thumby.display.fill(1)
        thumby.display.update()
        time.sleep(0.1)
        thumby.display.fill(0)
        thumby.display.update()

        # Destroy all ships
        for ship in ships:
            sx, sy, sz = ship
            hit_effects.append((sx, sy, sz, time.ticks_ms()))
        ships = []

def update_input():
    global rotation_x, rotation_y, rotation_z, last_shot_time
    if thumby.buttonU.pressed():
        rotation_x -= player_stats["rotation_speed"]
        if(rotation_x<-45):
            rotation_x=-45
    if thumby.buttonD.pressed():
        rotation_x += player_stats["rotation_speed"]
        if(rotation_x>45):
            rotation_x=45
    if thumby.buttonL.pressed():
        rotation_y += player_stats["rotation_speed"]
        if(rotation_y>45):
            rotation_y=45
    if thumby.buttonR.pressed():
        rotation_y -= player_stats["rotation_speed"]
        if(rotation_y<-45):
            rotation_y=-45
    if thumby.buttonA.justPressed():
        current_time = time.ticks_ms()
        if current_time - last_shot_time >= player_stats["time_between_shots"]:
            fire_lasers()
            last_shot_time = current_time
    if thumby.buttonB.justPressed():  # Add this block
        activate_smart_bomb()

def rotate(x, y, z, angle_x, angle_y, angle_z):
    x, y, z = rotate_x(x, y, z, angle_x)
    x, y, z = rotate_y(x, y, z, angle_y)
    x, y, z = rotate_z(x, y, z, angle_z)
    return x, y, z

def fire_lasers():
    global player_lasers
    thumby.audio.play(random.randrange(270, 300), 50)
    # Calculate direction vector towards where the player is looking
    direction_x, direction_y, direction_z = 0, 0, 1
    direction_x, direction_y, direction_z = rotate(direction_x, direction_y, direction_z, -rotation_x, -rotation_y, -rotation_z)

    # Fire lasers from two positions towards the center
    gun1_x, gun1_y, gun1_z = 5, -3, 0.1
    gun2_x, gun2_y, gun2_z = -5, -3, 0.1
    if (player_stats["extra_lasers"] > 0):
        gun3_x, gun3_y, gun3_z = 0, -3, 0.1

    # Calculate the transformed gun positions
    gun1_x, gun1_y, gun1_z = rotate(gun1_x, gun1_y, gun1_z, -rotation_x, -rotation_y, -rotation_z)
    gun2_x, gun2_y, gun2_z = rotate(gun2_x, gun2_y, gun2_z, -rotation_x, -rotation_y, -rotation_z)
    if (player_stats["extra_lasers"] > 0):
        gun3_x, gun3_y, gun3_z = rotate(gun3_x, gun3_y, gun3_z, -rotation_x, -rotation_y, -rotation_z)

    laser_speed = player_stats["laser_speed"]
    player_lasers.append((gun1_x, gun1_y, gun1_z, direction_x * laser_speed, direction_y * laser_speed, direction_z * laser_speed))
    player_lasers.append((gun2_x, gun2_y, gun2_z, direction_x * laser_speed, direction_y * laser_speed, direction_z * laser_speed))
    if (player_stats["extra_lasers"] > 0):
        player_lasers.append((gun3_x, gun3_y, gun3_z, direction_x * laser_speed, direction_y * laser_speed, direction_z * laser_speed))

# Update game state (move ships and lasers)
def update_game():
    global enemy_lasers, player_lasers, hit_effects, ships, score, kill_count, ships_passed, current_level
    spawnrate = 3 * (current_level + 1 + player_stats["hard_mode"])
    if random.randint(0, 100) < spawnrate:  # 3% chance to spawn a new ship each frame
        spawn_ship()
    
    new_ships = []
    ships_to_remove = set()
    
    # First check for collisions
    new_player_lasers = []
    for laser in player_lasers:
        x, y, z, vx, vy, vz = laser
        z += vz
        y += vy
        x += vx
        if z < 50:  # Check if laser is still within range
            new_player_lasers.append((x, y, z, vx, vy, vz))
            # Check for collision with ships
            for ship in ships:
                sx, sy, sz = ship
                if abs(sx - x) < 3 and abs(sy - y) < 3 and abs(sz - z) < 3:
                    hit_effects.append((sx, sy, sz, time.ticks_ms()))
                    ships_to_remove.add(ship)
                    kill_count += 1
                    break
    player_lasers = new_player_lasers

    # Update ship positions and remove hit ships
    for ship in ships:
        if ship not in ships_to_remove:
            x, y, z = ship
            z -= 0.35 * (current_level + 1)
            if z < 1:  # Check if ship has passed
                ships_passed += 1
                continue  # Skip adding this ship to new_ships
            new_ships.append((x, y, z))
            if random.randint(0, 100) < 20:  # 20% chance to fire a laser each frame
                vz = -3  # Velocity vector in z-direction (towards player) and faster
                if z != 0:
                    vx = (x / z) * vz
                    vy = (y / z) * vz
                else:
                    vx, vy = 0, 0
                enemy_lasers.append((x, y, z, vx, vy, vz))

    ships = new_ships

    # Update enemy lasers
    new_enemy_lasers = []
    for laser in enemy_lasers:
        x, y, z, vx, vy, vz = laser
        z += vz
        if z > 0:
            new_enemy_lasers.append((x, y, z, vx, vy, vz))
    enemy_lasers = new_enemy_lasers

    # Remove old hit effects
    hit_effects = [effect for effect in hit_effects if time.ticks_ms() - effect[3] < 1500]

def level_loop(level_data):
    global score, kill_count, ships_passed, min_shot_interval

    show_intro_screen(level_data["intro"])
    reset_level_variables()
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 30000:  # 30 seconds
        thumby.display.fill(0)  # Clear the screen
        update_input()
        update_game()
        draw_stars(rotation_x, rotation_y, rotation_z)
        draw_planets(rotation_x, rotation_y, rotation_z)
        draw_ships(rotation_x, rotation_y, rotation_z)
        draw_lasers(rotation_x, rotation_y, rotation_z, enemy_lasers)
        draw_lasers(rotation_x, rotation_y, rotation_z, player_lasers)
        draw_hit_effects(rotation_x, rotation_y, rotation_z)
        thumby.display.drawFilledRectangle(19,35,72,5,0)
        thumby.display.blit(cockpit, 0, 0, 72, 40, 0, 0, 0)
        thumby.display.drawText(f'K:{kill_count}', 22, 35, 1)
        thumby.display.drawText(f'D:{ships_passed}', 37, 35, 1)
        
        time_elapsed = time.ticks_diff(time.ticks_ms(), start_time) / 1000
        time_bar_length = int(15 * (time_elapsed / 30))
        
        remaining_ships = max(0, levels[current_level]["max_passed"] + player_stats["shield"] - ships_passed)
        ships_bar_length = int(15 * (remaining_ships / levels[current_level]["max_passed"]))
        
        thumby.display.drawLine(2, 39, 2 + time_bar_length, 39, 0)
        thumby.display.drawLine(54, 39, 54 + ships_bar_length, 39, 0)
        
        thumby.display.update()

    
    if ships_passed > level_data["max_passed"] + player_stats["shield"]:
        return False
    
    earned_money = kill_count * 10  # Example earning calculation
    show_shop_screen(earned_money)


    return True

def game_loop():
    global current_level, ships_passed, score, kill_count
    reset_level_variables()
    draw_stars(rotation_x, rotation_y, rotation_z)
    draw_planets(rotation_x, rotation_y, rotation_z)
    thumby.display.blit(cockpit, 0, 0, 72, 40, 0, 0, 0)
    thumby.display.drawText(f'X-Wing', 25, 35, 1)
    thumby.display.update()
    play_audio_sequence(sequence)
    while current_level < len(levels):
        ships_passed = 0
        score = 0
        kill_count = 0
        if not level_loop(levels[current_level]):
            show_game_over_screen()
            break
        current_level += 1
        if(current_level>len(levels)):
            you_win_screen()

game_loop()
