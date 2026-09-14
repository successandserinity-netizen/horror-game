import pygame
import random
import math
import os
import sys

pygame.init()

# ============================================================
# THE RECORDING 4.0
# THE HOUSE REMEMBERS
# ============================================================

WIDTH = 1000
HEIGHT = 650
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE RECORDING 4.0")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 22)
SMALL_FONT = pygame.font.SysFont("consolas", 17)
BIG_FONT = pygame.font.SysFont("consolas", 46, bold=True)

BLACK = (3, 3, 6)
WHITE = (235, 235, 235)
RED = (175, 20, 25)
DARK_RED = (70, 8, 12)
GRAY = (80, 80, 88)
GREEN = (50, 170, 80)
YELLOW = (210, 180, 50)
WALL = (12, 12, 16)
FLOOR = (32, 32, 38)

SAVE_FILE = "recording_save.txt"

# ============================================================
# SAVE
# ============================================================

completed_runs = 0
new_game_plus = False


def load_save():
    global completed_runs, new_game_plus

    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip().split(",")

        if len(data) >= 2:
            completed_runs = max(0, int(data[0]))
            new_game_plus = bool(int(data[1]))

    except (ValueError, OSError):
        completed_runs = 0
        new_game_plus = False


def save_progress():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{completed_runs},{int(new_game_plus)}")
    except OSError:
        pass


load_save()

# ============================================================
# PLAYER
# ============================================================

PLAYER_SIZE = 32

player = pygame.Rect(
    480,
    520,
    PLAYER_SIZE,
    PLAYER_SIZE
)

SPEED = 4

ROOM_BOUNDS = pygame.Rect(
    55,
    55,
    890,
    500
)

room = "hall"

# ============================================================
# OBJECTS
# ============================================================

hall_tv = pygame.Rect(420, 120, 150, 85)
vhs1 = pygame.Rect(760, 500, 35, 35)
key1 = pygame.Rect(150, 150, 25, 25)
hall_door = pygame.Rect(920, 260, 45, 120)

bedroom_tv = pygame.Rect(420, 120, 150, 85)
vhs2 = pygame.Rect(170, 150, 35, 35)
key2 = pygame.Rect(750, 430, 25, 25)

bedroom_hall_door = pygame.Rect(
    30,
    260,
    45,
    120
)

bedroom_basement_door = pygame.Rect(
    920,
    500,
    45,
    100
)

bed = pygame.Rect(
    300,
    320,
    300,
    160
)

basement_tv = pygame.Rect(
    250,
    130,
    180,
    100
)

power_switch = pygame.Rect(
    120,
    180,
    35,
    55
)

vhs3 = pygame.Rect(
    730,
    420,
    35,
    35
)

basement_exit = pygame.Rect(
    450,
    40,
    100,
    55
)

# ============================================================
# SECRET ROOM
# ============================================================

secret_door = pygame.Rect(
    850,
    120,
    70,
    100
)

secret_tv = pygame.Rect(
    400,
    120,
    180,
    100
)

vhs4 = pygame.Rect(
    760,
    450,
    35,
    35
)

secret_exit = pygame.Rect(
    450,
    40,
    100,
    55
)

vhs5 = pygame.Rect(
    740,
    280,
    35,
    35
)

fuse_rects = [
    pygame.Rect(600, 160, 30, 30),
    pygame.Rect(650, 160, 30, 30),
    pygame.Rect(700, 160, 30, 30)
]

# ============================================================
# ITEMS
# ============================================================

has_vhs1 = False
watched_vhs1 = False
has_key1 = False

has_vhs2 = False
watched_vhs2 = False
has_key2 = False

basement_power = False

has_vhs3 = False
watched_vhs3 = False

fuse1 = False
fuse2 = False
fuse3 = False

puzzle_complete = False

has_vhs4 = False
watched_vhs4 = False

has_vhs5 = False
watched_vhs5 = False


def reset_items():

    global has_vhs1, watched_vhs1, has_key1
    global has_vhs2, watched_vhs2, has_key2
    global basement_power
    global has_vhs3, watched_vhs3
    global fuse1, fuse2, fuse3, puzzle_complete
    global has_vhs4, watched_vhs4
    global has_vhs5, watched_vhs5

    has_vhs1 = False
    watched_vhs1 = False
    has_key1 = False

    has_vhs2 = False
    watched_vhs2 = False
    has_key2 = False

    basement_power = False

    has_vhs3 = False
    watched_vhs3 = False

    fuse1 = False
    fuse2 = False
    fuse3 = False
    puzzle_complete = False

    has_vhs4 = False
    watched_vhs4 = False

    has_vhs5 = False
    watched_vhs5 = False


# ============================================================
# HORROR
# ============================================================

creature_visible = False
creature_x = 800.0
creature_y = 300.0
creature_state = "idle"
creature_timer = 0
creature_chase_timer = 0

flash_timer = 0
screen_shake = 0

message = ""
message_timer = 0

fear_level = 10

# ============================================================
# HEALTH
# ============================================================

health = 100
MAX_HEALTH = 100

health_flash_timer = 0
health_shake_timer = 0

# ============================================================
# FLASHLIGHT
# ============================================================

battery = 100
flashlight_on = True
battery_timer = 0
flash_flicker_timer = 0

# ============================================================
# HORROR EVENTS
# ============================================================

random_event_timer = 0
tv_glitch_timer = 0

# ============================================================
# ADVANCED HORROR
# ============================================================

heartbeat_timer = 0

shadow_timer = 0
shadow_x = 0
shadow_y = 0
shadow_visible = False

house_event_timer = 0

# ============================================================
# LOOK AWAY
# ============================================================

look_away_timer = 0
look_event_count = 0

# ============================================================
# ENDINGS
# ============================================================

ending = False

normal_ending = False
bad_ending = False
loop_ending = False
secret_ending = False
true_ending = False
memory_ending = False
vhs5_ending = False
mary_shaw_ending = False

# NEW
death_ending = False


# ============================================================
# UTILITY
# ============================================================

def show_message(text, duration=180):

    global message
    global message_timer

    message = text
    message_timer = duration


def distance_to_player(x, y):

    return math.hypot(
        player.centerx - x,
        player.centery - y
    )


def draw_text(
    text,
    x,
    y,
    font=FONT,
    color=WHITE
):

    surface = font.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


def center_text(
    text,
    y,
    font=FONT,
    color=WHITE
):

    surface = font.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (
            WIDTH // 2 -
            surface.get_width() // 2,
            y
        )
    )


def interactable(rect):

    return player.colliderect(
        rect.inflate(20, 20)
    )


# ============================================================
# WALLS
# ============================================================

def draw_walls():

    pygame.draw.rect(
        screen,
        FLOOR,
        (0, 0, WIDTH, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        WALL,
        (0, 0, WIDTH, 50)
    )

    pygame.draw.rect(
        screen,
        WALL,
        (0, HEIGHT - 50, WIDTH, 50)
    )

    pygame.draw.rect(
        screen,
        WALL,
        (0, 0, 50, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        WALL,
        (WIDTH - 50, 0, 50, HEIGHT)
    )

    pygame.draw.line(
        screen,
        (55, 55, 62),
        (50, 100),
        (950, 100),
        2
    )

    pygame.draw.line(
        screen,
        (20, 20, 25),
        (50, 560),
        (950, 560),
        2
    )


# ============================================================
# TV
# ============================================================

def draw_tv(
    rect,
    creepy=False,
    memory=False,
    creature=False
):

    pygame.draw.rect(
        screen,
        (25, 25, 30),
        rect
    )

    pygame.draw.rect(
        screen,
        (5, 5, 8),
        rect,
        5
    )

    inner = pygame.Rect(
        rect.x + 12,
        rect.y + 10,
        rect.width - 24,
        rect.height - 25
    )

    if creature:

        pygame.draw.rect(
            screen,
            (10, 5, 12),
            inner
        )

        pygame.draw.ellipse(
            screen,
            (5, 5, 7),
            (
                inner.centerx - 22,
                inner.centery - 30,
                44,
                65
            )
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                inner.centerx - 10,
                inner.centery - 12
            ),
            4
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                inner.centerx + 10,
                inner.centery - 12
            ),
            4
        )

    elif tv_glitch_timer > 0:

        pygame.draw.rect(
            screen,
            (130, 130, 130),
            inner
        )

        for _ in range(9):

            y = random.randint(
                inner.top,
                inner.bottom - 1
            )

            pygame.draw.line(
                screen,
                (20, 20, 25),
                (inner.left, y),
                (inner.right, y),
                random.randint(1, 3)
            )

    elif memory:

        pygame.draw.rect(
            screen,
            (20, 25, 45),
            inner
        )

        draw_text(
            "YOU CAME BACK",
            inner.x + 15,
            inner.y + 25,
            SMALL_FONT
        )

    elif creepy:

        pygame.draw.rect(
            screen,
            (30, 5, 10),
            inner
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                inner.centerx - 25,
                inner.centery - 5
            ),
            6
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                inner.centerx + 25,
                inner.centery - 5
            ),
            6
        )

        pygame.draw.line(
            screen,
            RED,
            (
                inner.centerx - 25,
                inner.centery + 25
            ),
            (
                inner.centerx + 25,
                inner.centery + 25
            ),
            3
        )

    else:

        pygame.draw.rect(
            screen,
            (35, 35, 40),
            inner
        )

    pygame.draw.rect(
        screen,
        (20, 20, 22),
        (
            rect.x + 50,
            rect.bottom,
            80,
            15
        )
    )


# ============================================================
# OBJECT DRAWING
# ============================================================

def draw_vhs(rect, number):

    pygame.draw.rect(
        screen,
        (18, 18, 22),
        rect
    )

    pygame.draw.rect(
        screen,
        RED,
        rect,
        2
    )

    draw_text(
        str(number),
        rect.x + 11,
        rect.y + 5,
        SMALL_FONT
    )


def draw_key(rect):

    pygame.draw.rect(
        screen,
        YELLOW,
        rect
    )

    pygame.draw.circle(
        screen,
        FLOOR,
        rect.center,
        5
    )


def draw_fuse(rect, number):

    pygame.draw.rect(
        screen,
        (100, 100, 105),
        rect
    )

    pygame.draw.rect(
        screen,
        (160, 160, 165),
        rect,
        2
    )

    draw_text(
        str(number),
        rect.x + 8,
        rect.y + 3,
        SMALL_FONT
    )


# ============================================================
# CREATURE
# ============================================================

def spawn_creature(x=None, y=None):

    global creature_visible
    global creature_x
    global creature_y
    global creature_timer
    global creature_state

    creature_visible = True
    creature_state = "idle"

    if x is None:

        creature_x = random.randint(
            120,
            880
        )

    else:

        creature_x = max(
            70,
            min(930, x)
        )

    if y is None:

        creature_y = random.randint(
            100,
            540
        )

    else:

        creature_y = max(
            80,
            min(545, y)
        )

    creature_timer = random.randint(
        180,
        420
    )


def draw_creature():

    # Body
    pygame.draw.ellipse(
        screen,
        (8, 8, 11),
        (
            int(creature_x - 28),
            int(creature_y - 55),
            56,
            100
        )
    )

    # Head
    pygame.draw.ellipse(
        screen,
        (12, 12, 15),
        (
            int(creature_x - 24),
            int(creature_y - 70),
            48,
            45
        )
    )

    # Eyes
    pygame.draw.circle(
        screen,
        RED,
        (
            int(creature_x - 9),
            int(creature_y - 55)
        ),
        4
    )

    pygame.draw.circle(
        screen,
        RED,
        (
            int(creature_x + 9),
            int(creature_y - 55)
        ),
        4
    )


def update_creature():

    global creature_x
    global creature_y
    global creature_visible
    global creature_timer
    global creature_state
    global creature_chase_timer
    global fear_level
    global flash_timer
    global screen_shake

    global health
    global health_flash_timer
    global health_shake_timer
    global heartbeat_timer

    if not creature_visible or ending:
        return

    creature_timer -= 1

    d = distance_to_player(
        creature_x,
        creature_y
    )

    # ========================================================
    # IDLE
    # ========================================================

    if creature_state == "idle":

        if d < 320:

            chance = 2 + fear_level // 12

            if random.randint(
                1,
                100
            ) <= chance:

                creature_state = "chase"

                creature_chase_timer = random.randint(
                    90,
                    240
                )

                show_message(
                    "IT SAW YOU."
                )

                fear_level = min(
                    100,
                    fear_level + 4
                )

        if random.randint(
            1,
            100
        ) <= 3:

            angle = random.uniform(
                0,
                math.tau
            )

            creature_x += (
                math.cos(angle) * 2
            )

            creature_y += (
                math.sin(angle) * 2
            )

    # ========================================================
    # CHASE
    # ========================================================

    elif creature_state == "chase":

        creature_chase_timer -= 1

        dx = (
            player.centerx -
            creature_x
        )

        dy = (
            player.centery -
            creature_y
        )

        length = math.hypot(
            dx,
            dy
        )

        if length > 1:

            chase_speed = (
                1.8 +
                fear_level / 95
            )

            creature_x += (
                dx / length
            ) * chase_speed

            creature_y += (
                dy / length
            ) * chase_speed

        if creature_chase_timer <= 0:

            creature_state = "idle"

            show_message(
                "IT DISAPPEARED."
            )

    creature_x = max(
        65,
        min(935, creature_x)
    )

    creature_y = max(
        85,
        min(545, creature_y)
    )

    # ========================================================
    # CREATURE ATTACK
    # ========================================================

    if d < 55:

        damage = 20

        health = max(
            0,
            health - damage
        )

        health_flash_timer = 15
        health_shake_timer = 15

        heartbeat_timer = 25

        flash_timer = (
            12 +
            fear_level // 10
        )

        screen_shake = (
            10 +
            fear_level // 8
        )

        fear_level = min(
            100,
            fear_level + 10
        )

        show_message(
            "IT TOUCHED YOU."
        )

        creature_visible = False
        creature_state = "idle"

        # ====================================================
        # NEW DEATH ENDING
        # ====================================================

        if health <= 0:

            show_message(
                "THE HOUSE TOOK YOU."
            )

            trigger_ending(
                "death"
            )

            return

    # ========================================================
    # CREATURE VANISHES
    # ========================================================

    if creature_timer <= 0:

        creature_visible = False
        creature_state = "idle"


# ============================================================
# RANDOM HORROR EVENTS
# ============================================================

def random_horror_event():

    global random_event_timer
    global fear_level
    global tv_glitch_timer

    if ending:
        return

    random_event_timer += 1

    threshold = max(
        180,
        600 - fear_level * 3
    )

    if random_event_timer < threshold:
        return

    random_event_timer = 0

    chance = random.randint(
        1,
        10
    )

    messages = [
        "SOMETHING MOVED.",
        "DID YOU HEAR THAT?",
        "THE ROOM IS HOLDING ITS BREATH.",
        "THE HOUSE IS LISTENING.",
        "DON'T LOOK AT THE TV.",
        "SOMEONE IS BEHIND YOU."
    ]

    if chance <= 6:

        show_message(
            messages[chance - 1]
        )

        fear_level = min(
            100,
            fear_level + 1
        )

    elif chance <= 8:

        tv_glitch_timer = random.randint(
            20,
            45
        )

        show_message(
            "THE SIGNAL IS WRONG."
        )

        fear_level = min(
            100,
            fear_level + 2
        )

    else:

        spawn_creature(
            player.centerx +
            random.randint(-250, 250),

            player.centery +
            random.randint(-180, 180)
        )


# ============================================================
# SHADOW EVENT
# ============================================================

def shadow_event():

    global shadow_timer
    global shadow_x
    global shadow_y
    global shadow_visible
    global fear_level

    if ending:
        return

    shadow_timer += 1

    threshold = max(
        500,
        1400 - fear_level * 8
    )

    if shadow_timer < threshold:
        return

    shadow_timer = 0

    if random.randint(
        1,
        100
    ) > 35:

        return

    side = random.choice([
        "left",
        "right",
        "top"
    ])

    if side == "left":

        shadow_x = 75
        shadow_y = random.randint(
            150,
            500
        )

    elif side == "right":

        shadow_x = 900
        shadow_y = random.randint(
            150,
            500
        )

    else:

        shadow_x = random.randint(
            150,
            850
        )

        shadow_y = 80

    shadow_visible = True

    show_message(
        "DID SOMETHING JUST MOVE?"
    )

    fear_level = min(
        100,
        fear_level + 3
    )


def draw_shadow():

    if not shadow_visible:
        return

    pygame.draw.ellipse(
        screen,
        (5, 5, 7),
        (
            shadow_x - 18,
            shadow_y - 45,
            36,
            90
        )
    )

    pygame.draw.circle(
        screen,
        (8, 8, 10),
        (
            shadow_x - 7,
            shadow_y - 45
        ),
        3
    )

    pygame.draw.circle(
        screen,
        (8, 8, 10),
        (
            shadow_x + 7,
            shadow_y - 45
        ),
        3
    )


# ============================================================
# HOUSE REACTION
# ============================================================

def house_reaction():

    global house_event_timer
    global fear_level
    global tv_glitch_timer

    if ending:
        return

    house_event_timer += 1

    threshold = max(
        300,
        900 - fear_level * 5
    )

    if house_event_timer < threshold:
        return

    house_event_timer = 0

    event = random.randint(
        1,
        5
    )

    if event == 1:

        tv_glitch_timer = 20

        show_message(
            "THE HOUSE KNOWS YOU ARE AFRAID."
        )

        fear_level = min(
            100,
            fear_level + 2
        )

    elif event == 2:

        show_message(
            "THE FLOOR CREAKED BEHIND YOU."
        )

    elif event == 3:

        show_message(
            "SOMETHING JUST WALKED PAST."
        )

    elif event == 4:

        show_message(
            "THE HOUSE IS GETTING QUIETER."
        )

    else:

        show_message(
            "YOU ARE NOT ALONE."
        )

        fear_level = min(
            100,
            fear_level + 2
        )


# ============================================================
# HEARTBEAT
# ============================================================

def update_heartbeat():

    global heartbeat_timer

    if ending:
        return

    if fear_level >= 70:

        chance = max(
            30,
            180 - fear_level
        )

        if random.randint(
            1,
            chance
        ) == 1:

            heartbeat_timer = 8


def draw_heartbeat():

    global heartbeat_timer

    if heartbeat_timer <= 0:
        return

    intensity = min(
        90,
        30 + (fear_level - 70) * 2
    )

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (120, 0, 0, intensity)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    heartbeat_timer -= 1


# ============================================================
# FLASHLIGHT
# ============================================================

def draw_flashlight():

    if not flashlight_on or battery <= 0:
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 232)
    )

    radius = int(
        170 +
        battery * 0.35
    )

    if battery < 30:

        radius = (
            105 +
            battery
        )

    if flash_flicker_timer <= 0:

        pygame.draw.circle(
            overlay,
            (0, 0, 0, 0),
            player.center,
            radius
        )

    else:

        pygame.draw.circle(
            overlay,
            (0, 0, 0, 0),
            player.center,
            max(
                70,
                radius // 2
            )
        )

    screen.blit(
        overlay,
        (0, 0)
    )


# ============================================================
# HEALTH BAR
# ============================================================

def draw_health_bar():

    global health_shake_timer

    x = 20
    y = 105

    width = 220
    height = 18

    shake_x = 0
    shake_y = 0

    if health_shake_timer > 0:

        shake_x = random.randint(
            -5,
            5
        )

        shake_y = random.randint(
            -3,
            3
        )

        health_shake_timer -= 1

    x += shake_x
    y += shake_y

    draw_text(
        "HEALTH",
        x,
        y - 21,
        SMALL_FONT
    )

    pygame.draw.rect(
        screen,
        (45, 45, 45),
        (
            x,
            y,
            width,
            height
        )
    )

    health_width = int(
        width *
        (health / MAX_HEALTH)
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            x,
            y,
            health_width,
            height
        )
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (
            x,
            y,
            width,
            height
        ),
        2
    )


def draw_health_flash():

    global health_flash_timer

    if health_flash_timer <= 0:
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    alpha = min(
        120,
        health_flash_timer * 8
    )

    overlay.fill(
        (255, 0, 0, alpha)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    health_flash_timer -= 1


# ============================================================
# COLLISION
# ============================================================

def room_obstacles():

    if room == "hall":
        return []

    if room == "bedroom":
        return [bed]

    if room == "basement":
        return []

    if room == "secret":
        return []

    return []


def move_player(dx, dy):

    player.x += dx

    for obstacle in room_obstacles():

        if player.colliderect(obstacle):

            if dx > 0:
                player.right = obstacle.left

            elif dx < 0:
                player.left = obstacle.right

    player.y += dy

    for obstacle in room_obstacles():

        if player.colliderect(obstacle):

            if dy > 0:
                player.bottom = obstacle.top

            elif dy < 0:
                player.top = obstacle.bottom

    player.clamp_ip(
        ROOM_BOUNDS
    )


# ============================================================
# UI
# ============================================================

def draw_ui():

    draw_text(
        f"ROOM: {room.upper()}",
        20,
        15,
        SMALL_FONT
    )

    draw_text(
        f"BATTERY: {battery}%",
        20,
        38,
        SMALL_FONT
    )

    draw_text(
        f"FEAR: {fear_level}%",
        20,
        61,
        SMALL_FONT,
        RED
    )

    draw_health_bar()

    draw_text(
        "WASD / ARROWS = MOVE",
        20,
        610,
        SMALL_FONT
    )

    draw_text(
        "E = INTERACT   F = FLASHLIGHT",
        680,
        610,
        SMALL_FONT
    )


def draw_message():

    if message_timer <= 0:
        return

    box = pygame.Rect(
        110,
        555,
        780,
        60
    )

    pygame.draw.rect(
        screen,
        (5, 5, 8),
        box
    )

    pygame.draw.rect(
        screen,
        DARK_RED,
        box,
        2
    )

    text = FONT.render(
        message,
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            box.centerx -
            text.get_width() // 2,
            box.y + 17
        )
    )


def draw_interaction_hint():

    if ending:
        return

    targets = []

    if room == "hall":

        targets = [
            (
                vhs1,
                not has_vhs1
            ),
            (
                hall_tv,
                has_vhs1 and not watched_vhs1
            ),
            (
                key1,
                watched_vhs1 and not has_key1
            ),
            (
                hall_door,
                True
            )
        ]

    elif room == "bedroom":

        targets = [
            (
                vhs2,
                not has_vhs2
            ),
            (
                bedroom_tv,
                has_vhs2 and not watched_vhs2
            ),
            (
                key2,
                watched_vhs2 and not has_key2
            ),
            (
                bedroom_basement_door,
                True
            ),
            (
                bedroom_hall_door,
                True
            )
        ]

    elif room == "basement":

        targets = [
            (
                power_switch,
                not basement_power
            ),
            (
                vhs3,
                basement_power and not has_vhs3
            ),
            (
                basement_tv,
                basement_power
                and has_vhs3
                and not watched_vhs3
            ),
            (
                secret_door,
                puzzle_complete
            ),
            (
                basement_exit,
                True
            )
        ]

        for i, fuse in enumerate(
            fuse_rects
        ):

            fuse_state = [
                fuse1,
                fuse2,
                fuse3
            ][i]

            targets.append(
                (
                    fuse,
                    basement_power
                    and not fuse_state
                )
            )

    elif room == "secret":

        targets = [
            (
                vhs4,
                not has_vhs4
            ),
            (
                secret_tv,
                has_vhs4
                and not watched_vhs4
            ),
            (
                vhs5,
                watched_vhs4
                and not has_vhs5
            ),
            (
                secret_tv,
                has_vhs5
                and not watched_vhs5
            ),
            (
                secret_exit,
                True
            )
        ]

    for rect, active in targets:

        if active and interactable(rect):

            draw_text(
                "E",
                rect.centerx - 6,
                rect.top - 25,
                SMALL_FONT,
                YELLOW
            )

            break


# ============================================================
# ENDINGS
# ============================================================

def finish_run():

    global completed_runs
    global new_game_plus

    completed_runs += 1
    new_game_plus = True

    save_progress()


def trigger_ending(kind):

    global ending

    global normal_ending
    global bad_ending
    global loop_ending
    global secret_ending
    global true_ending
    global memory_ending
    global vhs5_ending
    global mary_shaw_ending
    global death_ending

    if ending:
        return

    ending = True

    normal_ending = (
        kind == "normal"
    )

    bad_ending = (
        kind == "bad"
    )

    loop_ending = (
        kind == "loop"
    )

    secret_ending = (
        kind == "secret"
    )

    true_ending = (
        kind == "true"
    )

    memory_ending = (
        kind == "memory"
    )

    vhs5_ending = (
        kind == "vhs5"
    )

    mary_shaw_ending = (
        kind == "mary_shaw"
    )

    death_ending = (
        kind == "death"
    )

    finish_run()


def choose_basement_ending():

    roll = random.randint(
        1,
        1000
    )

    if has_vhs5 and watched_vhs5:

        trigger_ending(
            "vhs5"
        )

    elif roll == 1:

        trigger_ending(
            "secret"
        )

    elif (
        new_game_plus
        and roll <= 30
    ):

        trigger_ending(
            "memory"
        )

    elif roll <= 80:

        trigger_ending(
            "true"
        )

    elif roll <= 130:

        trigger_ending(
            "loop"
        )

    elif roll <= 230:

        trigger_ending(
            "bad"
        )

    else:

        trigger_ending(
            "normal"
        )


def show_ending():

    screen.fill(
        BLACK
    )

    # ========================================================
    # NEW: YOU DIED
    # ========================================================

    if death_ending:

        # Dark red background
        pygame.draw.rect(
            screen,
            (18, 2, 5),
            (0, 0, WIDTH, HEIGHT)
        )

        # Subtle red pulses
        pulse = random.randint(
            0,
            25
        )

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (120, 0, 10, pulse)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        center_text(
            "YOU DIED",
            145,
            BIG_FONT,
            RED
        )

        center_text(
            "THE HOUSE TOOK YOU.",
            250,
            FONT,
            WHITE
        )

        center_text(
            "YOU COULDN'T ESCAPE.",
            305,
            FONT,
            GRAY
        )

        center_text(
            "THE RECORDING CONTINUES.",
            360,
            FONT,
            RED
        )

        center_text(
            "ENDING: DEATH",
            445,
            SMALL_FONT,
            YELLOW
        )

        center_text(
            "PRESS R TO PLAY AGAIN",
            540,
            FONT,
            WHITE
        )

        return

    # ========================================================
    # MARY SHAW
    # ========================================================

    if mary_shaw_ending:

        center_text(
            "YOU GOT TO",
            100,
            FONT,
            RED
        )

        center_text(
            "MARY SHAW'S HOUSE",
            155,
            BIG_FONT,
            RED
        )

        center_text(
            "THE HOUSE WAS NEVER THE END.",
            270
        )

        center_text(
            "IT WAS THE BEGINNING.",
            325
        )

        center_text(
            "THE RECORDING WAS MADE HERE.",
            380,
            FONT,
            RED
        )

        center_text(
            "VERY HARD ENDING",
            450,
            SMALL_FONT,
            YELLOW
        )

        center_text(
            "YOU FOUND WHAT WAS NEVER MEANT TO BE FOUND.",
            490,
            SMALL_FONT
        )

    elif secret_ending:

        center_text(
            "THE HOUSE BURNS DOWN.",
            160,
            BIG_FONT,
            RED
        )

        center_text(
            "THE RECORDING SURVIVED.",
            250
        )

        center_text(
            "YOU DIDN'T.",
            310,
            FONT,
            RED
        )

    elif vhs5_ending:

        center_text(
            "THE RECORDING NEVER ENDS.",
            160,
            BIG_FONT,
            RED
        )

        center_text(
            "YOU FOUND THE ORIGINAL TAPE.",
            260
        )

        center_text(
            "NOW IT HAS YOUR FACE.",
            320,
            FONT,
            RED
        )

    elif memory_ending:

        center_text(
            "THE HOUSE REMEMBERS.",
            160,
            BIG_FONT,
            RED
        )

        center_text(
            "YOU ESCAPED LAST TIME.",
            250
        )

        center_text(
            "THIS TIME, IT FOLLOWED.",
            310
        )

    elif true_ending:

        center_text(
            "TRUE ENDING",
            160,
            BIG_FONT,
            RED
        )

        center_text(
            "THE RECORDING WAS NEVER THE TAPE.",
            250
        )

        center_text(
            "IT WAS THE HOUSE.",
            310
        )

        center_text(
            "AND NOW IT KNOWS YOU.",
            370
        )

    elif loop_ending:

        center_text(
            "ENDING 3",
            160,
            BIG_FONT
        )

        center_text(
            "YOU ESCAPED.",
            250
        )

        center_text(
            "YOU OPENED YOUR FRONT DOOR.",
            310
        )

        center_text(
            "THE HOUSE WAS ON THE OTHER SIDE.",
            370
        )

    elif bad_ending:

        center_text(
            "ENDING 2",
            160,
            BIG_FONT
        )

        center_text(
            "YOU ESCAPED THE HOUSE.",
            250
        )

        center_text(
            "BUT SOMETHING FOLLOWED YOU.",
            310
        )

        center_text(
            "THE RECORDING NEVER ENDS.",
            370,
            FONT,
            RED
        )

    else:

        center_text(
            "ENDING 1",
            160,
            BIG_FONT
        )

        center_text(
            "YOU ESCAPED.",
            260
        )

        center_text(
            "THE TELEVISION IS STILL PLAYING.",
            320
        )

    center_text(
        "PRESS R TO PLAY AGAIN",
        540
    )


# ============================================================
# INTERACTION
# ============================================================

def handle_interaction():

    global has_vhs1
    global watched_vhs1
    global has_key1

    global has_vhs2
    global watched_vhs2
    global has_key2

    global basement_power
    global has_vhs3
    global watched_vhs3

    global fuse1
    global fuse2
    global fuse3

    global has_vhs4
    global watched_vhs4

    global has_vhs5
    global watched_vhs5

    global fear_level
    global flash_timer
    global screen_shake
    global room

    # ========================================================
    # HALL
    # ========================================================

    if room == "hall":

        if (
            not has_vhs1
            and interactable(vhs1)
        ):

            has_vhs1 = True

            show_message(
                "YOU FOUND VHS 1."
            )

        elif (
            has_vhs1
            and not watched_vhs1
            and interactable(hall_tv)
        ):

            watched_vhs1 = True

            show_message(
                "THE SCREEN SHOWS YOU."
            )

            spawn_creature(
                760,
                250
            )

            flash_timer = 8

        elif (
            watched_vhs1
            and not has_key1
            and interactable(key1)
        ):

            has_key1 = True

            show_message(
                "YOU FOUND A STRANGE KEY."
            )

        elif interactable(hall_door):

            if has_key1:

                room = "bedroom"

                player.x = 100
                player.y = 300

                show_message(
                    "THE BEDROOM DOOR OPENS."
                )

            else:

                show_message(
                    "THE DOOR IS LOCKED."
                )

    # ========================================================
    # BEDROOM
    # ========================================================

    elif room == "bedroom":

        if (
            not has_vhs2
            and interactable(vhs2)
        ):

            has_vhs2 = True

            show_message(
                "ANOTHER VHS..."
            )

        elif (
            has_vhs2
            and not watched_vhs2
            and interactable(bedroom_tv)
        ):

            watched_vhs2 = True

            show_message(
                "WHY DID YOU WATCH IT?"
            )

            spawn_creature(
                700,
                400
            )

        elif (
            watched_vhs2
            and not has_key2
            and interactable(key2)
        ):

            has_key2 = True

            show_message(
                "THE KEY IS FREEZING COLD."
            )

        elif interactable(
            bedroom_basement_door
        ):

            if has_key2:

                room = "basement"

                player.x = 120
                player.y = 500

                show_message(
                    "SOMETHING IS WAITING DOWNSTAIRS."
                )

            else:

                show_message(
                    "YOU NEED ANOTHER KEY."
                )

        elif interactable(
            bedroom_hall_door
        ):

            room = "hall"

            player.x = 850
            player.y = 300

    # ========================================================
    # BASEMENT
    # ========================================================

    elif room == "basement":

        if (
            not basement_power
            and interactable(power_switch)
        ):

            basement_power = True

            show_message(
                "THE POWER CAME BACK ON."
            )

        elif (
            basement_power
            and not has_vhs3
            and interactable(vhs3)
        ):

            has_vhs3 = True

            show_message(
                "VHS 3. THE TV IS WAITING."
            )

            spawn_creature(
                500,
                350
            )

        elif (
            basement_power
            and has_vhs3
            and not watched_vhs3
            and interactable(basement_tv)
        ):

            watched_vhs3 = True

            show_message(
                "THE RECORDING KNOWS YOU ARE HERE."
            )

            spawn_creature(
                800,
                300
            )

            flash_timer = 15
            screen_shake = 10

        elif (
            basement_power
            and not fuse1
            and interactable(fuse_rects[0])
        ):

            fuse1 = True

            show_message(
                "FUSE 1 INSTALLED."
            )

        elif (
            basement_power
            and not fuse2
            and interactable(fuse_rects[1])
        ):

            fuse2 = True

            show_message(
                "FUSE 2 INSTALLED."
            )

        elif (
            basement_power
            and not fuse3
            and interactable(fuse_rects[2])
        ):

            fuse3 = True

            show_message(
                "FUSE 3 INSTALLED."
            )

        elif (
            puzzle_complete
            and interactable(secret_door)
        ):

            room = "secret"

            player.x = 100
            player.y = 300

            show_message(
                "YOU FOUND A ROOM THAT WASN'T ON THE MAP."
            )

            fear_level = min(
                100,
                fear_level + 8
            )

        elif interactable(
            basement_exit
        ):

            if not watched_vhs3:

                show_message(
                    "THE RECORDING ISN'T FINISHED."
                )

            elif not puzzle_complete:

                show_message(
                    "SOMETHING IS STILL MISSING."
                )

            else:

                choose_basement_ending()

    # ========================================================
    # SECRET ROOM
    # ========================================================

    elif room == "secret":

        if (
            not has_vhs4
            and interactable(vhs4)
        ):

            has_vhs4 = True

            show_message(
                "YOU FOUND THE TAPE THAT WASN'T SUPPOSED TO EXIST."
            )

            fear_level = min(
                100,
                fear_level + 5
            )

            spawn_creature(
                650,
                300
            )

        elif (
            has_vhs4
            and not watched_vhs4
            and interactable(secret_tv)
        ):

            watched_vhs4 = True

            show_message(
                "THIS IS NOT A RECORDING OF THE HOUSE."
            )

            fear_level = min(
                100,
                fear_level + 10
            )

            flash_timer = 20

            spawn_creature(
                750,
                350
            )

        elif (
            watched_vhs4
            and not has_vhs5
            and interactable(vhs5)
        ):

            has_vhs5 = True

            show_message(
                "THAT TAPE WAS HIDDEN BEHIND THE WALL."
            )

        elif (
            has_vhs5
            and not watched_vhs5
            and interactable(secret_tv)
        ):

            watched_vhs5 = True

            show_message(
                "YOU WERE NEVER SUPPOSED TO SEE THIS."
            )

            flash_timer = 25
            screen_shake = 12

            spawn_creature(
                600,
                300
            )

        # ====================================================
        # SECRET ROOM EXIT
        # ====================================================

        elif interactable(
            secret_exit
        ):

            if (
                watched_vhs4
                and not has_vhs5
                and fear_level >= 90
                and battery <= 10
            ):

                trigger_ending(
                    "mary_shaw"
                )

            elif watched_vhs5:

                trigger_ending(
                    "vhs5"
                )

            elif watched_vhs4:

                trigger_ending(
                    "true"
                )

            else:

                show_message(
                    "THE TV IS WAITING."
                )


# ============================================================
# DRAW ROOM
# ============================================================

def draw_room():

    # ========================================================
    # HALL
    # ========================================================

    if room == "hall":

        draw_walls()

        draw_tv(
            hall_tv,
            creepy=watched_vhs1,
            memory=new_game_plus,
            creature=(
                creature_visible
                and random.randint(1, 5) == 1
            )
        )

        if not has_vhs1:
            draw_vhs(
                vhs1,
                1
            )

        if watched_vhs1 and not has_key1:
            draw_key(key1)

        pygame.draw.rect(
            screen,
            (70, 50, 40),
            hall_door
        )

        draw_text(
            "BEDROOM",
            850,
            225,
            SMALL_FONT
        )

    # ========================================================
    # BEDROOM
    # ========================================================

    elif room == "bedroom":

        draw_walls()

        pygame.draw.rect(
            screen,
            (50, 50, 65),
            bed
        )

        pygame.draw.rect(
            screen,
            (80, 80, 100),
            (
                330,
                320,
                240,
                60
            )
        )

        draw_tv(
            bedroom_tv,
            creepy=watched_vhs2,
            memory=new_game_plus,
            creature=(
                creature_visible
                and random.randint(1, 5) == 1
            )
        )

        if not has_vhs2:
            draw_vhs(
                vhs2,
                2
            )

        if watched_vhs2 and not has_key2:
            draw_key(key2)

        pygame.draw.rect(
            screen,
            (45, 30, 30),
            bedroom_basement_door
        )

        draw_text(
            "BASEMENT",
            850,
            525,
            SMALL_FONT
        )

        pygame.draw.rect(
            screen,
            (45, 30, 30),
            bedroom_hall_door
        )

        draw_text(
            "HALL",
            45,
            225,
            SMALL_FONT
        )

    # ========================================================
    # BASEMENT
    # ========================================================

    elif room == "basement":

        draw_walls()

        pygame.draw.rect(
            screen,
            (10, 10, 14),
            (
                55,
                55,
                890,
                500
            )
        )

        if basement_power:

            draw_tv(
                basement_tv,
                creepy=watched_vhs3,
                memory=(
                    new_game_plus
                    and not watched_vhs3
                ),
                creature=(
                    creature_visible
                    and random.randint(1, 4) == 1
                )
            )

            if watched_vhs3:

                draw_text(
                    "THE RECORDING IS WATCHING YOU",
                    235,
                    255,
                    SMALL_FONT,
                    RED
                )

            else:

                draw_text(
                    "INSERT VHS 3",
                    335,
                    255,
                    SMALL_FONT
                )

        else:

            pygame.draw.rect(
                screen,
                (15, 15, 18),
                basement_tv
            )

            pygame.draw.rect(
                screen,
                GRAY,
                basement_tv,
                5
            )

        pygame.draw.rect(
            screen,
            GREEN if basement_power else GRAY,
            power_switch
        )

        draw_text(
            "POWER",
            105,
            145,
            SMALL_FONT
        )

        if (
            basement_power
            and not has_vhs3
        ):

            draw_vhs(
                vhs3,
                3
            )

        if basement_power:

            states = [
                fuse1,
                fuse2,
                fuse3
            ]

            for i in range(3):

                if states[i]:

                    pygame.draw.rect(
                        screen,
                        GREEN,
                        fuse_rects[i]
                    )

                else:

                    draw_fuse(
                        fuse_rects[i],
                        i + 1
                    )

            draw_text(
                "FUSES",
                610,
                125,
                SMALL_FONT
            )

        pygame.draw.rect(
            screen,
            (55, 35, 35),
            basement_exit
        )

        draw_text(
            "EXIT",
            478,
            65,
            SMALL_FONT
        )

        # ====================================================
        # SECRET DOOR
        # ====================================================

        if puzzle_complete:

            pygame.draw.rect(
                screen,
                (70, 15, 20),
                secret_door
            )

            pygame.draw.rect(
                screen,
                (150, 25, 30),
                secret_door,
                3
            )

            pygame.draw.circle(
                screen,
                (180, 170, 80),
                (
                    secret_door.right - 15,
                    secret_door.centery
                ),
                5
            )

            draw_text(
                "SECRET",
                secret_door.x - 3,
                secret_door.y - 28,
                SMALL_FONT,
                RED
            )

        else:

            pygame.draw.rect(
                screen,
                (35, 12, 15),
                secret_door,
                2
            )

    # ========================================================
    # SECRET ROOM
    # ========================================================

    elif room == "secret":

        draw_walls()

        pygame.draw.rect(
            screen,
            (12, 6, 15),
            (
                55,
                55,
                890,
                500
            )
        )

        draw_tv(
            secret_tv,
            creepy=watched_vhs4,
            memory=True,
            creature=(
                creature_visible
                and random.randint(1, 3) == 1
            )
        )

        if not has_vhs4:

            draw_vhs(
                vhs4,
                4
            )

        if watched_vhs4 and not has_vhs5:

            draw_vhs(
                vhs5,
                5
            )

            draw_text(
                "SOMETHING IS HERE",
                690,
                250,
                SMALL_FONT,
                RED
            )

        pygame.draw.rect(
            screen,
            (55, 35, 35),
            secret_exit
        )

        draw_text(
            "EXIT",
            478,
            65,
            SMALL_FONT
        )

    # ========================================================
    # CREATURE
    # ========================================================

    if creature_visible:

        draw_creature()

    # ========================================================
    # PLAYER
    # ========================================================

    pygame.draw.rect(
        screen,
        (180, 180, 185),
        player
    )

    pygame.draw.rect(
        screen,
        (30, 30, 35),
        (
            player.x + 7,
            player.y + 8,
            5,
            5
        )
    )

    pygame.draw.rect(
        screen,
        (30, 30, 35),
        (
            player.x + 20,
            player.y + 8,
            5,
            5
        )
    )


# ============================================================
# RESET
# ============================================================

def reset_game():

    global room

    global creature_visible
    global creature_state
    global creature_timer
    global creature_x
    global creature_y

    global flash_timer
    global screen_shake

    global message
    global message_timer
    global fear_level

    global health
    global health_flash_timer
    global health_shake_timer

    global heartbeat_timer

    global shadow_timer
    global shadow_x
    global shadow_y
    global shadow_visible

    global house_event_timer

    global look_away_timer
    global look_event_count

    global battery
    global flashlight_on
    global battery_timer
    global flash_flicker_timer

    global random_event_timer
    global tv_glitch_timer

    global ending

    global normal_ending
    global bad_ending
    global loop_ending
    global secret_ending
    global true_ending
    global memory_ending
    global vhs5_ending
    global mary_shaw_ending
    global death_ending

    room = "hall"

    player.x = 480
    player.y = 520

    reset_items()

    # Creature
    creature_visible = False
    creature_state = "idle"
    creature_timer = 0
    creature_x = 800
    creature_y = 300

    # Screen effects
    flash_timer = 0
    screen_shake = 0

    # Messages
    message = ""
    message_timer = 0

    # Fear
    fear_level = min(
        100,
        10 + completed_runs * 5
    )

    # Health
    health = MAX_HEALTH
    health_flash_timer = 0
    health_shake_timer = 0

    # Heartbeat
    heartbeat_timer = 0

    # Shadows
    shadow_timer = 0
    shadow_x = 0
    shadow_y = 0
    shadow_visible = False

    # House
    house_event_timer = 0

    # Look-away system
    look_away_timer = 0
    look_event_count = 0

    # Flashlight
    battery = 100
    flashlight_on = True
    battery_timer = 0
    flash_flicker_timer = 0

    # Horror events
    random_event_timer = 0
    tv_glitch_timer = 0

    # Endings
    ending = False

    normal_ending = False
    bad_ending = False
    loop_ending = False
    secret_ending = False
    true_ending = False
    memory_ending = False
    vhs5_ending = False
    mary_shaw_ending = False

    # NEW
    death_ending = False


# ============================================================
# MAIN LOOP
# ============================================================

reset_game()

running = True

while running:

    clock.tick(FPS)

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if (
                ending
                and event.key == pygame.K_r
            ):

                reset_game()

                if new_game_plus:

                    show_message(
                        "YOU CAME BACK.",
                        300
                    )

            elif (
                not ending
                and event.key == pygame.K_f
            ):

                if battery > 0:

                    flashlight_on = (
                        not flashlight_on
                    )

            elif (
                not ending
                and event.key == pygame.K_e
            ):

                handle_interaction()

    # ========================================================
    # MOVEMENT
    # ========================================================

    if not ending:

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if (
            keys[pygame.K_a]
            or keys[pygame.K_LEFT]
        ):

            dx -= SPEED

        if (
            keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
        ):

            dx += SPEED

        if (
            keys[pygame.K_w]
            or keys[pygame.K_UP]
        ):

            dy -= SPEED

        if (
            keys[pygame.K_s]
            or keys[pygame.K_DOWN]
        ):

            dy += SPEED

        if dx != 0 and dy != 0:

            factor = 1 / math.sqrt(2)

            dx *= factor
            dy *= factor

        move_player(
            round(dx),
            round(dy)
        )

    # ========================================================
    # CREATURE
    # ========================================================

    update_creature()

    # ========================================================
    # LOOK AWAY
    # ========================================================

    if watched_vhs2 and not ending:

        look_away_timer += 1

        if (
            look_away_timer > 700
            and look_event_count == 0
        ):

            look_event_count = 1

            show_message(
                "SOMETHING MOVED BEHIND YOU."
            )

            spawn_creature(
                player.centerx + 230,
                player.centery
            )

        elif (
            look_away_timer > 1400
            and look_event_count == 1
        ):

            look_event_count = 2

            show_message(
                "IT IS LEARNING WHERE YOU GO."
            )

            spawn_creature(
                player.centerx - 220,
                player.centery
            )

    # ========================================================
    # BATTERY
    # ========================================================

    if (
        flashlight_on
        and battery > 0
        and not ending
    ):

        battery_timer += 1

        if battery_timer >= 120:

            battery -= 1
            battery_timer = 0

        if (
            battery <= 20
            and random.randint(
                1,
                45
            ) == 1
        ):

            flash_flicker_timer = random.randint(
                4,
                10
            )

        else:

            flash_flicker_timer = max(
                0,
                flash_flicker_timer - 1
            )

    # ========================================================
    # HORROR SYSTEMS
    # ========================================================

    random_horror_event()

    shadow_event()

    house_reaction()

    update_heartbeat()

    # ========================================================
    # SHADOW DISAPPEARS WHEN APPROACHED
    # ========================================================

    if shadow_visible:

        shadow_distance = math.hypot(
            player.centerx - shadow_x,
            player.centery - shadow_y
        )

        if shadow_distance < 180:

            shadow_visible = False

            show_message(
                "THERE IS NOTHING THERE."
            )

    # ========================================================
    # TIMERS
    # ========================================================

    message_timer = max(
        0,
        message_timer - 1
    )

    flash_timer = max(
        0,
        flash_timer - 1
    )

    screen_shake = max(
        0,
        screen_shake - 1
    )

    tv_glitch_timer = max(
        0,
        tv_glitch_timer - 1
    )

    # ========================================================
    # FUSE PUZZLE
    # ========================================================

    if (
        fuse1
        and fuse2
        and fuse3
        and not puzzle_complete
    ):

        puzzle_complete = True

        show_message(
            "THE SECRET DOOR UNLOCKED."
        )

        fear_level = min(
            100,
            fear_level + 5
        )

    # ========================================================
    # DRAW
    # ========================================================

    if ending:

        show_ending()

    else:

        screen.fill(
            BLACK
        )

        draw_room()

        # Shadow appears before flashlight
        draw_shadow()

        draw_flashlight()

        # Heartbeat overlay
        draw_heartbeat()

        # Normal white flash
        if flash_timer > 0:

            flash = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            flash.fill(
                WHITE
            )

            flash.set_alpha(
                min(
                    180,
                    80 +
                    flash_timer * 5
                )
            )

            screen.blit(
                flash,
                (0, 0)
            )

        # Damage flash
        draw_health_flash()

        draw_ui()

        draw_message()

        draw_interaction_hint()

    # ========================================================
    # SCREEN SHAKE
    # ========================================================

    if (
        screen_shake > 0
        and not ending
    ):

        offset_x = random.randint(
            -screen_shake,
            screen_shake
        )

        offset_y = random.randint(
            -screen_shake,
            screen_shake
        )

        shaken = screen.copy()

        screen.fill(
            BLACK
        )

        screen.blit(
            shaken,
            (
                offset_x,
                offset_y
            )
        )

    pygame.display.flip()


pygame.quit()
sys.exit()
