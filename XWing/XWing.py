import thumby
import math
import random
import time

# Initialize the screen
thumby.display.setFPS(30)
random.seed(time.ticks_ms())

# Define screen dimensions
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40

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

# Initialize stars, ships, and lasers
stars = [(random.randint(-50, 50), random.randint(-30, 30), random.randint(10, 50)) for _ in range(100)]
ships = []  # List to store enemy ships
enemy_lasers = []  # List to store enemy lasers
player_lasers = []  # List to store player lasers
hit_effects = []  # List to store hit effects

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

# Render ships
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
            # Draw ship as an "X" that grows larger as it approaches
            thumby.display.drawLine(screen_x - size, screen_y - size, screen_x + size, screen_y + size, 1)
            thumby.display.drawLine(screen_x - size, screen_y + size, screen_x + size, screen_y - size, 1)

# Render lasers
def draw_lasers(rotation_x, rotation_y, rotation_z, lasers):
    for laser in lasers:
        x, y, z, vx, vy, vz = laser

        # Rotate start point
        rotated_x, rotated_y, rotated_z = rotate_x(x, y, z, rotation_x)
        rotated_x, rotated_y, rotated_z = rotate_y(rotated_x, rotated_y, rotated_z, rotation_y)
        rotated_x, rotated_y, rotated_z = rotate_z(rotated_x, rotated_y, rotated_z, rotation_z)

        # Rotate direction vector
        #rotated_vx, rotated_vy, rotated_vz = rotate_x(vx, vy, vz, rotation_x)
        #rotated_vx, rotated_vy, rotated_vz = rotate_y(rotated_vx, rotated_vy, rotated_vz, rotation_y)
        #rotated_vx, rotated_vy, rotated_vz = rotate_z(rotated_vx, rotated_vy, rotated_vz, rotation_z)
        
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
        size = max(1, int(size_factor * 4))  # Scale the size based on distance
        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            thumby.display.drawRectangle(screen_x - size // 2, screen_y - size // 2, size, size, 1)


# Handle input and update rotation
rotation_x, rotation_y, rotation_z = 0, 0, 0

def update_input():
    global rotation_x, rotation_y, rotation_z
    if thumby.buttonU.pressed():
        rotation_x -= 5
        if(rotation_x<-30):
            rotation_x=-30
    if thumby.buttonD.pressed():
        rotation_x += 5
        if(rotation_x>30):
            rotation_x=30
    if thumby.buttonL.pressed():
        rotation_y += 5
        if(rotation_y>45):
            rotation_y=45
    if thumby.buttonR.pressed():
        rotation_y -= 5
        if(rotation_y<-45):
            rotation_y=-45
    if thumby.buttonA.justPressed():
        fire_lasers()

def rotate(x, y, z, angle_x, angle_y, angle_z):
    x, y, z = rotate_x(x, y, z, angle_x)
    x, y, z = rotate_y(x, y, z, angle_y)
    x, y, z = rotate_z(x, y, z, angle_z)
    return x, y, z

def fire_lasers():
    global player_lasers
    # Calculate direction vector towards where the player is looking
    direction_x, direction_y, direction_z = 0, 0, 1
    direction_x, direction_y, direction_z = rotate(direction_x, direction_y, direction_z, -rotation_x, -rotation_y, -rotation_z)

    # Fire lasers from two positions towards the center
    gun1_x, gun1_y, gun1_z = 5, -3, 0.1
    gun2_x, gun2_y, gun2_z = -5, -3, 0.1

    # Calculate the transformed gun positions
    gun1_x, gun1_y, gun1_z = rotate(gun1_x, gun1_y, gun1_z, -rotation_x, -rotation_y, -rotation_z)
    gun2_x, gun2_y, gun2_z = rotate(gun2_x, gun2_y, gun2_z, -rotation_x, -rotation_y, -rotation_z)

    laser_speed = 3
    player_lasers.append((gun1_x, gun1_y, gun1_z, direction_x * laser_speed, direction_y * laser_speed, direction_z * laser_speed))
    player_lasers.append((gun2_x, gun2_y, gun2_z, direction_x * laser_speed, direction_y * laser_speed, direction_z * laser_speed))

# Update game state (move ships and lasers)
def update_game():
    global enemy_lasers, player_lasers, hit_effects, ships
    if random.randint(0, 100) < 3:  # 3% chance to spawn a new ship each frame
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
                if abs(sx - x) < 2 and abs(sy - y) < 2 and abs(sz - z) < 2:
                    hit_effects.append((sx, sy, sz, time.ticks_ms()))
                    ships_to_remove.add(ship)
                    break
    player_lasers = new_player_lasers

    # Update ship positions and remove hit ships
    for ship in ships:
        if ship not in ships_to_remove:
            x, y, z = ship
            z -= 1
            if z < 1:  # Reset the ship position when it gets too close
                x = random.randint(-25, 25)
                y = random.randint(-15, 15)
                z = 50
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

# Main game loop
def game_loop():
    while True:
        thumby.display.fill(0)  # Clear the screen
        update_input()
        update_game()
        draw_stars(rotation_x, rotation_y, rotation_z)
        draw_ships(rotation_x, rotation_y, rotation_z)
        draw_lasers(rotation_x, rotation_y, rotation_z, enemy_lasers)
        draw_lasers(rotation_x, rotation_y, rotation_z, player_lasers)
        draw_hit_effects(rotation_x, rotation_y, rotation_z)
        thumby.display.update()

game_loop()