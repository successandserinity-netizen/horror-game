import pygame
import random
import math
import os
import sys

pygame.init()

# ============================================================
# THE RECORDING 4.1
# THE HOUSE REMEMBERS
# ============================================================

WIDTH = 1000
HEIGHT = 650
FPS = 60

pygame.display.set_caption("THE RECORDING 4.1")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ============================================================
# FONTS
# ============================================================

FONT = pygame.font.SysFont("consolas", 22)
SMALL_FONT = pygame.font.SysFont("consolas", 17)
BIG_FONT = pygame.font.SysFont("consolas", 46, bold=True)

# ============================================================
# COLORS
# ============================================================

BLACK = (3, 3, 6)
WHITE = (235, 235, 235)
RED = (175, 20, 25)
DARK_RED = (70, 8, 12)
GRAY = (80, 80, 88)
GREEN = (50, 170, 80)
YELLOW = (210, 180, 50)
WALL = (12, 12, 16)
FLOOR = (32, 32, 38)

# ============================================================
# SAVE SYSTEM
# ============================================================

SAVE_FILE = "recording_save.txt"

completed_runs = 0
new_game_plus = False


def load_save():
    global completed_runs, new_game_plus

    if not os.path.exists(SAVE_FILE):
        completed_runs = 0
        new_game_plus = False
        return

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip().split(",")

        if len(data) >= 1:
            completed_runs = max(0, int(data[0]))

        if len(data) >= 2:
            new_game_plus = bool(int(data[1]))

    except Exception:
        completed_runs = 0
        new_game_plus = False


def save_progress():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            f.write(
                f"{completed_runs},{int(new_game_plus)}"
            )
    except Exception:
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
bedroom_hall_door = pygame.Rect(30, 260, 45, 120)
bedroom_basement_door = pygame.Rect(920, 500, 45, 100)

bed = pygame.Rect(300, 320, 300, 160)

basement_tv = pygame.Rect(250, 130, 180, 100)
power_switch = pygame.Rect(120, 180, 35, 55)
vhs3 = pygame.Rect(730, 420, 35, 35)
basement_exit = pygame.Rect(450, 40, 100, 55)
secret_door = pygame.Rect(850, 120, 70, 100)

secret_tv = pygame.Rect(400, 120, 180, 100)
vhs4 = pygame.Rect(760, 450, 35, 35)
vhs5 = pygame.Rect(740, 280, 35, 35)
secret_exit = pygame.Rect(450, 40, 100, 55)

fuse_rects = [
    pygame.Rect(600, 160, 30, 30),
    pygame.Rect(650, 160, 30, 30),
    pygame.Rect(700, 160, 30, 30),
]

# ============================================================
# ITEM STATE
# ============================================================

has_vhs1 = False
has_vhs2 = False
has_vhs3 = False
has_vhs4 = False
has_vhs5 = False

watched_vhs1 = False
watched_vhs2 = False
watched_vhs3 = False
watched_vhs4 = False
watched_vhs5 = False

has_key1 = False
has_key2 = False

basement_power = False

fuse1 = False
fuse2 = False
fuse3 = False

puzzle_complete = False


def reset_items():

    global has_vhs1
    global has_vhs2
    global has_vhs3
    global has_vhs4
    global has_vhs5

    global watched_vhs1
    global watched_vhs2
    global watched_vhs3
    global watched_vhs4
    global watched_vhs5

    global has_key1
    global has_key2

    global basement_power

    global fuse1
    global fuse2
    global fuse3

    global puzzle_complete

    has_vhs1 = False
    has_vhs2 = False
    has_vhs3 = False
    has_vhs4 = False
    has_vhs5 = False

    watched_vhs1 = False
    watched_vhs2 = False
    watched_vhs3 = False
    watched_vhs4 = False
    watched_vhs5 = False

    has_key1 = False
    has_key2 = False

    basement_power = False

    fuse1 = False
    fuse2 = False
    fuse3 = False

    puzzle_complete = False


# ============================================================
# HORROR STATE
# ============================================================

creature_visible = False

creature_x = 800.0
creature_y = 300.0

creature_state = "idle"
creature_timer = 0
creature_chase_timer = 0

# ============================================================
# AFK GHOST SYSTEM
# ============================================================

AFK_WARNING = 90
AFK_LIMIT = 180
AFK_HUNT_TIME = 420

afk_timer = 0
afk_stage = 0

afk_hunt_active = False
afk_hunt_timer = 0

last_player_x = player.x
last_player_y = player.y

player_activity = False

# ============================================================
# HORROR EFFECTS
# ============================================================

flash_timer = 0
screen_shake = 0

message = ""
message_timer = 0

fear_level = 10

# ============================================================
# HEALTH
# ============================================================

MAX_HEALTH = 100
health = MAX_HEALTH

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
# HORROR TIMERS
# ============================================================

random_event_timer = 0
tv_glitch_timer = 0

heartbeat_timer = 0

shadow_timer = 0
shadow_x = 0
shadow_y = 0
shadow_visible = False

house_event_timer = 0

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
death_ending = False


# ============================================================
# UTILITY
# ============================================================

def show_message(text, duration=150):

    global message
    global message_timer

    message = text
    message_timer = duration


def distance_to_player(x, y):

    return math.hypot(
        player.centerx - x,
        player.centery - y
    )


def interactable(rect):

    return player.colliderect(
        rect.inflate(20, 20)
    )


def draw_text(
    text,
    font,
    color,
    x,
    y,
    center=False
):

    surf = font.render(
        text,
        True,
        color
    )

    if center:
        rect = surf.get_rect(
            center=(x, y)
        )
    else:
        rect = surf.get_rect(
            topleft=(x, y)
        )

    screen.blit(surf, rect)


# ============================================================
# PLAYER ACTIVITY / AFK SYSTEM
# ============================================================

def register_player_activity():

    global afk_timer
    global afk_stage
    global player_activity

    afk_timer = 0
    afk_stage = 0
    player_activity = True


def update_afk_system():

    global afk_timer
    global afk_stage
    global afk_hunt_active
    global afk_hunt_timer

    global last_player_x
    global last_player_y
    global player_activity

    # FIX:
    # These variables must be global because this function
    # changes them.
    global creature_state
    global creature_chase_timer

    global fear_level

    if ending:

        afk_timer = 0
        afk_stage = 0
        player_activity = False

        return

    moved = (
        player.x != last_player_x
        or player.y != last_player_y
    )

    # --------------------------------------------------------
    # PLAYER MOVED / ACTIVITY
    # --------------------------------------------------------

    if moved or player_activity:

        if moved:

            afk_timer = 0
            afk_stage = 0

            # Moving breaks the special AFK hunt.
            # The ghost can still chase normally for a short time.
            if afk_hunt_active:

                afk_hunt_active = False
                afk_hunt_timer = 0

                if creature_visible:

                    creature_state = "chase"

                    if creature_chase_timer < 120:
                        creature_chase_timer = 120

        else:

            afk_timer = 0
            afk_stage = 0

        last_player_x = player.x
        last_player_y = player.y

        player_activity = False

        return

    # --------------------------------------------------------
    # PLAYER HAS NOT MOVED
    # --------------------------------------------------------

    afk_timer += 1

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    if (
        afk_timer >= AFK_WARNING
        and afk_stage < 1
    ):

        afk_stage = 1

        show_message(
            "THE HOUSE NOTICED YOU STOPPED.",
            150
        )

        fear_level = min(
            100,
            fear_level + 5
        )

    # --------------------------------------------------------
    # AFK HUNT
    # --------------------------------------------------------

    if (
        afk_timer >= AFK_LIMIT
        and afk_stage < 2
    ):

        afk_stage = 2

        start_afk_hunt()


def start_afk_hunt():

    global creature_visible
    global creature_x
    global creature_y

    global creature_state
    global creature_timer
    global creature_chase_timer

    global afk_hunt_active
    global afk_hunt_timer

    global fear_level

    angle = random.uniform(
        0,
        math.pi * 2
    )

    distance = random.randint(
        190,
        260
    )

    creature_x = (
        player.centerx
        + math.cos(angle) * distance
    )

    creature_y = (
        player.centery
        + math.sin(angle) * distance
    )

    creature_x = max(
        70,
        min(930, creature_x)
    )

    creature_y = max(
        80,
        min(545, creature_y)
    )

    creature_visible = True
    creature_state = "chase"

    creature_timer = AFK_HUNT_TIME
    creature_chase_timer = AFK_HUNT_TIME

    afk_hunt_active = True
    afk_hunt_timer = AFK_HUNT_TIME

    fear_level = min(
        100,
        fear_level + 12
    )

    if (
        room == "secret"
        or watched_vhs4
    ):

        show_message(
            "IT WAS WAITING FOR YOU.",
            180
        )

    else:

        show_message(
            "DON'T STAND STILL.",
            180
        )


# ============================================================
# CREATURE
# ============================================================

def spawn_creature(x=None, y=None):

    global creature_visible
    global creature_x
    global creature_y

    global creature_state
    global creature_timer
    global creature_chase_timer

    global afk_hunt_active
    global afk_hunt_timer

    if x is None:
        x = random.randint(
            100,
            900
        )

    if y is None:
        y = random.randint(
            100,
            520
        )

    creature_x = max(
        70,
        min(930, float(x))
    )

    creature_y = max(
        80,
        min(545, float(y))
    )

    creature_visible = True
    creature_state = "idle"

    creature_timer = random.randint(
        180,
        420
    )

    creature_chase_timer = 0

    afk_hunt_active = False
    afk_hunt_timer = 0


def update_creature():

    global creature_visible
    global creature_x
    global creature_y

    global creature_state
    global creature_timer
    global creature_chase_timer

    global health
    global health_flash_timer
    global health_shake_timer

    global fear_level
    global screen_shake
    global heartbeat_timer

    global afk_hunt_active
    global afk_hunt_timer

    global afk_stage

    if ending:
        return

    if not creature_visible:
        return

    # ========================================================
    # AFK HUNT
    # ========================================================

    if afk_hunt_active:

        afk_hunt_timer -= 1

        dx = player.centerx - creature_x
        dy = player.centery - creature_y

        dist = math.hypot(
            dx,
            dy
        )

        if dist > 0:

            dx /= dist
            dy /= dist

        speed = (
            2.4
            + fear_level / 70.0
        )

        if room == "secret":
            speed += 0.5

        creature_x += dx * speed
        creature_y += dy * speed

        creature_state = "chase"

        # ----------------------------------------------------
        # ATTACK
        # ----------------------------------------------------

        if dist < 55:

            damage = 20

            health -= damage
            health = max(
                0,
                health
            )

            health_flash_timer = 25
            health_shake_timer = 20

            screen_shake = max(
                screen_shake,
                12
            )

            heartbeat_timer = 30

            fear_level = min(
                100,
                fear_level + 10
            )

            show_message(
                "IT TOUCHED YOU.",
                120
            )

            creature_visible = False
            afk_hunt_active = False
            afk_hunt_timer = 0
            afk_stage = 0

            if health <= 0:

                show_message(
                    "THE HOUSE TOOK YOU.",
                    180
                )

                trigger_ending(
                    "death"
                )

            return

        # ----------------------------------------------------
        # HUNT TIMEOUT
        # ----------------------------------------------------

        if afk_hunt_timer <= 0:

            afk_hunt_active = False
            creature_visible = False
            creature_state = "idle"

            show_message(
                "IT DISAPPEARED.",
                100
            )

        return

    # ========================================================
    # NORMAL CREATURE
    # ========================================================

    creature_timer -= 1

    d = distance_to_player(
        creature_x,
        creature_y
    )

    if creature_state == "idle":

        if d < 320:

            chance = (
                2
                + fear_level // 12
            )

            if random.randint(
                1,
                100
            ) <= chance:

                creature_state = "chase"

                creature_chase_timer = random.randint(
                    90,
                    240
                )

                fear_level = min(
                    100,
                    fear_level + 4
                )

        # Random wandering
        if random.randint(
            1,
            120
        ) == 1:

            creature_x += random.randint(
                -40,
                40
            )

            creature_y += random.randint(
                -40,
                40
            )

            creature_x = max(
                70,
                min(930, creature_x)
            )

            creature_y = max(
                80,
                min(545, creature_y)
            )

    elif creature_state == "chase":

        creature_chase_timer -= 1

        dx = player.centerx - creature_x
        dy = player.centery - creature_y

        dist = math.hypot(
            dx,
            dy
        )

        if dist > 0:

            dx /= dist
            dy /= dist

        speed = (
            1.8
            + fear_level / 95.0
        )

        creature_x += dx * speed
        creature_y += dy * speed

        if creature_chase_timer <= 0:

            creature_state = "idle"

            show_message(
                "IT DISAPPEARED.",
                100
            )

    # ========================================================
    # NORMAL ATTACK
    # ========================================================

    d = distance_to_player(
        creature_x,
        creature_y
    )

    if d < 55:

        damage = 20

        health -= damage

        health = max(
            0,
            health
        )

        health_flash_timer = 25
        health_shake_timer = 20

        screen_shake = max(
            screen_shake,
            10
        )

        heartbeat_timer = 30

        fear_level = min(
            100,
            fear_level + 10
        )

        show_message(
            "IT TOUCHED YOU.",
            120
        )

        creature_visible = False

        if health <= 0:

            show_message(
                "THE HOUSE TOOK YOU.",
                180
            )

            trigger_ending(
                "death"
            )

    # ========================================================
    # NORMAL CREATURE TIMEOUT
    # ========================================================

    if creature_timer <= 0:

        creature_visible = False
        creature_state = "idle"

        if not ending:

            show_message(
                "IT DISAPPEARED.",
                100
            )


# ============================================================
# HORROR EVENTS
# ============================================================

def random_horror_event():

    global random_event_timer
    global tv_glitch_timer
    global fear_level

    random_event_timer += 1

    threshold = max(
        180,
        600 - fear_level * 3
    )

    if random_event_timer < threshold:
        return

    random_event_timer = 0

    roll = random.randint(
        1,
        100
    )

    if roll <= 20:

        show_message(
            "SOMETHING MOVED.",
            120
        )

        fear_level = min(
            100,
            fear_level + 2
        )

    elif roll <= 40:

        show_message(
            "DID YOU HEAR THAT?",
            120
        )

        fear_level = min(
            100,
            fear_level + 2
        )

    elif roll <= 55:

        show_message(
            "THE ROOM IS HOLDING ITS BREATH.",
            140
        )

    elif roll <= 70:

        show_message(
            "THE HOUSE IS LISTENING.",
            140
        )

        fear_level = min(
            100,
            fear_level + 3
        )

    elif roll <= 85:

        show_message(
            "DON'T LOOK AT THE TV.",
            140
        )

        tv_glitch_timer = 45

    elif roll <= 95:

        show_message(
            "SOMEONE IS BEHIND YOU.",
            120
        )

        fear_level = min(
            100,
            fear_level + 4
        )

    else:

        if not creature_visible:

            spawn_creature(
                player.centerx
                + random.randint(-250, 250),
                player.centery
                + random.randint(-180, 180)
            )

            show_message(
                "IT FOUND YOU.",
                150
            )


def shadow_event():

    global shadow_timer
    global shadow_x
    global shadow_y
    global shadow_visible
    global fear_level

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

        shadow_x = (
            player.left
            - random.randint(80, 160)
        )

        shadow_y = player.centery

    elif side == "right":

        shadow_x = (
            player.right
            + random.randint(80, 160)
        )

        shadow_y = player.centery

    else:

        shadow_x = player.centerx

        shadow_y = (
            player.top
            - random.randint(80, 150)
        )

    shadow_visible = True

    fear_level = min(
        100,
        fear_level + 3
    )

    show_message(
        "DID SOMETHING JUST MOVE?",
        120
    )


def house_reaction():

    global house_event_timer
    global fear_level
    global tv_glitch_timer

    house_event_timer += 1

    threshold = max(
        300,
        900 - fear_level * 5
    )

    if house_event_timer < threshold:
        return

    house_event_timer = 0

    roll = random.randint(
        1,
        4
    )

    if roll == 1:

        show_message(
            "THE HOUSE IS LISTENING.",
            130
        )

        fear_level = min(
            100,
            fear_level + 3
        )

    elif roll == 2:

        show_message(
            "THE SIGNAL IS WRONG.",
            120
        )

        tv_glitch_timer = 60

    elif roll == 3:

        show_message(
            "YOU ARE NOT ALONE.",
            120
        )

        fear_level = min(
            100,
            fear_level + 4
        )

    else:

        show_message(
            "THE HOUSE REMEMBERS.",
            150
        )


# ============================================================
# FLASHLIGHT
# ============================================================

def draw_flashlight():

    if not flashlight_on:
        return

    darkness = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    darkness.fill(
        (0, 0, 0, 232)
    )

    radius = int(
        170 + battery * 0.35
    )

    if battery <= 20:
        radius -= 30

    if flash_flicker_timer > 0:
        radius //= 2

    pygame.draw.circle(
        darkness,
        (0, 0, 0, 0),
        player.center,
        radius
    )

    screen.blit(
        darkness,
        (0, 0)
    )


# ============================================================
# DRAWING
# ============================================================

def draw_walls():

    pygame.draw.rect(
        screen,
        WALL,
        ROOM_BOUNDS,
        10
    )


def draw_tv(rect, active=False):

    pygame.draw.rect(
        screen,
        (10, 10, 12),
        rect
    )

    pygame.draw.rect(
        screen,
        GRAY,
        rect,
        3
    )

    if active:

        pygame.draw.rect(
            screen,
            (35, 35, 40),
            rect.inflate(-12, -12)
        )

        for y in range(
            rect.top + 10,
            rect.bottom - 10,
            7
        ):

            pygame.draw.line(
                screen,
                (65, 65, 70),
                (rect.left + 8, y),
                (rect.right - 8, y),
                1
            )


def draw_vhs(rect, number):

    pygame.draw.rect(
        screen,
        (25, 25, 28),
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
        SMALL_FONT,
        WHITE,
        rect.centerx,
        rect.centery,
        True
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


def draw_fuse(
    rect,
    number,
    installed
):

    color = (
        GREEN
        if installed
        else GRAY
    )

    pygame.draw.rect(
        screen,
        color,
        rect
    )

    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        2
    )

    draw_text(
        str(number),
        SMALL_FONT,
        BLACK,
        rect.centerx,
        rect.centery,
        True
    )


def draw_creature():

    if not creature_visible:
        return

    x = int(creature_x)
    y = int(creature_y)

    # Shadow
    pygame.draw.ellipse(
        screen,
        (5, 5, 7),
        pygame.Rect(
            x - 25,
            y + 22,
            50,
            15
        )
    )

    # Body
    pygame.draw.ellipse(
        screen,
        (5, 5, 8),
        pygame.Rect(
            x - 18,
            y - 35,
            36,
            70
        )
    )

    # Head
    pygame.draw.circle(
        screen,
        (7, 7, 10),
        (x, y - 40),
        22
    )

    # Eyes
    pygame.draw.circle(
        screen,
        RED,
        (x - 8, y - 43),
        3
    )

    pygame.draw.circle(
        screen,
        RED,
        (x + 8, y - 43),
        3
    )


def draw_shadow():

    if not shadow_visible:
        return

    pygame.draw.ellipse(
        screen,
        (5, 5, 8),
        pygame.Rect(
            int(shadow_x) - 22,
            int(shadow_y) - 40,
            44,
            80
        )
    )


def draw_player():

    pygame.draw.rect(
        screen,
        (150, 150, 160),
        player
    )

    pygame.draw.rect(
        screen,
        BLACK,
        player,
        2
    )


# ============================================================
# ROOM DRAWING
# ============================================================

def draw_room():

    screen.fill(FLOOR)

    draw_walls()

    if room == "hall":

        draw_tv(
            hall_tv,
            watched_vhs1
        )

        if not has_vhs1:
            draw_vhs(
                vhs1,
                1
            )

        if not has_key1:
            draw_key(key1)

        pygame.draw.rect(
            screen,
            DARK_RED if not has_key1 else GRAY,
            hall_door
        )

    elif room == "bedroom":

        draw_tv(
            bedroom_tv,
            watched_vhs2
        )

        if not has_vhs2:
            draw_vhs(
                vhs2,
                2
            )

        if not has_key2:
            draw_key(key2)

        pygame.draw.rect(
            screen,
            (50, 45, 50),
            bed
        )

        pygame.draw.rect(
            screen,
            GRAY,
            bedroom_hall_door
        )

        pygame.draw.rect(
            screen,
            DARK_RED if not has_key2 else GRAY,
            bedroom_basement_door
        )

    elif room == "basement":

        draw_tv(
            basement_tv,
            watched_vhs3
        )

        pygame.draw.rect(
            screen,
            YELLOW if not basement_power else GREEN,
            power_switch
        )

        if not has_vhs3:
            draw_vhs(
                vhs3,
                3
            )

        for i, rect in enumerate(
            fuse_rects
        ):

            installed = [
                fuse1,
                fuse2,
                fuse3
            ][i]

            draw_fuse(
                rect,
                i + 1,
                installed
            )

        pygame.draw.rect(
            screen,
            GREEN if puzzle_complete else DARK_RED,
            basement_exit
        )

        pygame.draw.rect(
            screen,
            GREEN if puzzle_complete else DARK_RED,
            secret_door
        )

    elif room == "secret":

        draw_tv(
            secret_tv,
            watched_vhs4 or watched_vhs5
        )

        if not has_vhs4:
            draw_vhs(
                vhs4,
                4
            )

        if not has_vhs5:
            draw_vhs(
                vhs5,
                5
            )

        pygame.draw.rect(
            screen,
            GREEN if watched_vhs4 else DARK_RED,
            secret_exit
        )

    draw_shadow()
    draw_creature()
    draw_player()


# ============================================================
# UI
# ============================================================

def draw_health_bar():

    x = 20
    y = 20

    width = 230
    height = 20

    pygame.draw.rect(
        screen,
        BLACK,
        (
            x - 2,
            y - 2,
            width + 4,
            height + 4
        )
    )

    health_width = int(
        width
        * (health / MAX_HEALTH)
    )

    if health > 50:

        health_color = GREEN

    elif health > 25:

        health_color = YELLOW

    else:

        health_color = RED

    pygame.draw.rect(
        screen,
        health_color,
        (
            x,
            y,
            health_width,
            height
        )
    )

    draw_text(
        f"HEALTH {health}",
        SMALL_FONT,
        WHITE,
        x,
        y + 24
    )


def draw_ui():

    draw_health_bar()

    draw_text(
        f"BATTERY {battery}%",
        SMALL_FONT,
        WHITE,
        20,
        65
    )

    draw_text(
        f"FEAR {fear_level}",
        SMALL_FONT,
        WHITE,
        20,
        88
    )

    draw_text(
        f"ROOM: {room.upper()}",
        SMALL_FONT,
        GRAY,
        WIDTH - 190,
        20
    )

    draw_text(
        "WASD / ARROWS = MOVE",
        SMALL_FONT,
        GRAY,
        20,
        HEIGHT - 65
    )

    draw_text(
        "E = INTERACT",
        SMALL_FONT,
        GRAY,
        20,
        HEIGHT - 43
    )

    draw_text(
        "F = FLASHLIGHT",
        SMALL_FONT,
        GRAY,
        20,
        HEIGHT - 21
    )

    if (
        afk_stage == 1
        and not ending
    ):

        draw_text(
            "MOVEMENT IS IMPORTANT.",
            SMALL_FONT,
            RED,
            WIDTH - 250,
            HEIGHT - 35
        )


def draw_message():

    if message_timer <= 0:
        return

    overlay = pygame.Surface(
        (WIDTH, 80),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 150)
    )

    screen.blit(
        overlay,
        (
            0,
            HEIGHT // 2 - 40
        )
    )

    draw_text(
        message,
        FONT,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2,
        True
    )


# ============================================================
# ENDINGS
# ============================================================

def finish_run():

    global completed_runs
    global new_game_plus

    completed_runs += 1

    if completed_runs >= 1:
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

    ending = True

    normal_ending = False
    bad_ending = False
    loop_ending = False
    secret_ending = False
    true_ending = False
    memory_ending = False
    vhs5_ending = False
    mary_shaw_ending = False
    death_ending = False

    if kind == "normal":

        normal_ending = True

    elif kind == "bad":

        bad_ending = True

    elif kind == "loop":

        loop_ending = True

    elif kind == "secret":

        secret_ending = True

    elif kind == "true":

        true_ending = True

    elif kind == "memory":

        memory_ending = True

    elif kind == "vhs5":

        vhs5_ending = True

    elif kind == "mary_shaw":

        mary_shaw_ending = True

    elif kind == "death":

        death_ending = True

    finish_run()


def choose_basement_ending():

    roll = random.randint(
        1,
        1000
    )

    if watched_vhs5:

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

    screen.fill(BLACK)

    if death_ending:

        draw_text(
            "YOU DIED",
            BIG_FONT,
            RED,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "THE HOUSE TOOK YOU.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "YOU COULDN'T ESCAPE.",
            FONT,
            GRAY,
            WIDTH // 2,
            290,
            True
        )

        draw_text(
            "THE RECORDING CONTINUES.",
            FONT,
            GRAY,
            WIDTH // 2,
            330,
            True
        )

        draw_text(
            "ENDING: DEATH",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    elif mary_shaw_ending:

        draw_text(
            "THE HOUSE REMEMBERS.",
            BIG_FONT,
            RED,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "YOU STAYED TOO LONG.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "SHE WAS ALREADY THERE.",
            FONT,
            GRAY,
            WIDTH // 2,
            290,
            True
        )

        draw_text(
            "ENDING: MARY SHAW",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    elif vhs5_ending:

        draw_text(
            "THE FIFTH RECORDING",
            BIG_FONT,
            RED,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "YOU FOUND WHAT WAS NEVER MEANT TO BE FOUND.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: VHS 5",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    elif secret_ending:

        draw_text(
            "THE TRUTH",
            BIG_FONT,
            RED,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "THE HOUSE WAS RECORDING YOU.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: SECRET",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    elif memory_ending:

        draw_text(
            "YOU REMEMBER.",
            BIG_FONT,
            RED,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "YOU HAVE BEEN HERE BEFORE.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: MEMORY",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    elif true_ending:

        draw_text(
            "THE RECORDING ENDS.",
            BIG_FONT,
            WHITE,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "YOU MADE IT OUT.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: TRUE",
            FONT,
            GREEN,
            WIDTH // 2,
            400,
            True
        )

    elif loop_ending:

        draw_text(
            "YOU ESCAPED.",
            BIG_FONT,
            WHITE,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "BUT THE RECORDING STARTS AGAIN.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: LOOP",
            FONT,
            YELLOW,
            WIDTH // 2,
            400,
            True
        )

    elif bad_ending:

        draw_text(
            "YOU LEFT THE HOUSE.",
            BIG_FONT,
            WHITE,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "BUT SOMETHING CAME WITH YOU.",
            FONT,
            WHITE,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: BAD",
            FONT,
            RED,
            WIDTH // 2,
            400,
            True
        )

    else:

        draw_text(
            "YOU ESCAPED.",
            BIG_FONT,
            WHITE,
            WIDTH // 2,
            170,
            True
        )

        draw_text(
            "THE HOUSE GOES QUIET.",
            FONT,
            GRAY,
            WIDTH // 2,
            250,
            True
        )

        draw_text(
            "ENDING: NORMAL",
            FONT,
            WHITE,
            WIDTH // 2,
            400,
            True
        )

    draw_text(
        f"COMPLETED RUNS: {completed_runs}",
        SMALL_FONT,
        GRAY,
        WIDTH // 2,
        470,
        True
    )

    draw_text(
        "PRESS R TO PLAY AGAIN",
        SMALL_FONT,
        WHITE,
        WIDTH // 2,
        530,
        True
    )


# ============================================================
# INTERACTION
# ============================================================

def handle_interaction():

    global room

    global has_vhs1
    global has_vhs2
    global has_vhs3
    global has_vhs4
    global has_vhs5

    global watched_vhs1
    global watched_vhs2
    global watched_vhs3
    global watched_vhs4
    global watched_vhs5

    global has_key1
    global has_key2

    global basement_power

    global fuse1
    global fuse2
    global fuse3

    global puzzle_complete

    global fear_level
    global tv_glitch_timer

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
                "VHS TAPE 1 FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(hall_tv):

            if (
                has_vhs1
                and not watched_vhs1
            ):

                watched_vhs1 = True

                show_message(
                    "THE RECORDING SHOWS THE HALL.",
                    150
                )

                tv_glitch_timer = 70

                fear_level = min(
                    100,
                    fear_level + 8
                )

                if not creature_visible:

                    spawn_creature(
                        player.centerx + 180,
                        player.centery
                    )

                register_player_activity()

                return

        if (
            not has_key1
            and interactable(key1)
        ):

            has_key1 = True

            show_message(
                "BEDROOM KEY FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(hall_door):

            if has_key1:

                room = "bedroom"

                player.x = 70
                player.y = 300

                register_player_activity()

            else:

                show_message(
                    "THE DOOR IS LOCKED.",
                    100
                )

            return

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
                "VHS TAPE 2 FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(bedroom_tv):

            if (
                has_vhs2
                and not watched_vhs2
            ):

                watched_vhs2 = True

                show_message(
                    "SOMETHING IS WRONG WITH THIS RECORDING.",
                    160
                )

                tv_glitch_timer = 80

                fear_level = min(
                    100,
                    fear_level + 10
                )

                if not creature_visible:

                    spawn_creature(
                        player.centerx + 200,
                        player.centery
                    )

                register_player_activity()

                return

        if (
            not has_key2
            and interactable(key2)
        ):

            has_key2 = True

            show_message(
                "BASEMENT KEY FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(bedroom_hall_door):

            room = "hall"

            player.x = 880
            player.y = 300

            register_player_activity()

            return

        if interactable(bedroom_basement_door):

            if has_key2:

                room = "basement"

                player.x = 70
                player.y = 520

                register_player_activity()

            else:

                show_message(
                    "THE DOOR IS LOCKED.",
                    100
                )

            return

    # ========================================================
    # BASEMENT
    # ========================================================

    elif room == "basement":

        if interactable(power_switch):

            if not basement_power:

                basement_power = True

                show_message(
                    "THE POWER IS BACK.",
                    140
                )

                fear_level = min(
                    100,
                    fear_level + 5
                )

            else:

                show_message(
                    "THE POWER IS ALREADY ON.",
                    100
                )

            register_player_activity()

            return

        if (
            not has_vhs3
            and interactable(vhs3)
        ):

            has_vhs3 = True

            show_message(
                "VHS TAPE 3 FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(basement_tv):

            if (
                has_vhs3
                and not watched_vhs3
            ):

                if not basement_power:

                    show_message(
                        "THE TV HAS NO POWER.",
                        110
                    )

                else:

                    watched_vhs3 = True

                    show_message(
                        "THE BASEMENT WAS ON THE TAPE.",
                        150
                    )

                    tv_glitch_timer = 80

                    fear_level = min(
                        100,
                        fear_level + 10
                    )

                register_player_activity()

                return

        # ----------------------------------------------------
        # FUSE 1
        # ----------------------------------------------------

        if interactable(fuse_rects[0]):

            if (
                basement_power
                and not fuse1
            ):

                fuse1 = True

                show_message(
                    "FUSE 1 INSTALLED.",
                    100
                )

            else:

                show_message(
                    "NOTHING HAPPENS.",
                    80
                )

            register_player_activity()

            return

        # ----------------------------------------------------
        # FUSE 2
        # ----------------------------------------------------

        if interactable(fuse_rects[1]):

            if (
                basement_power
                and not fuse2
            ):

                fuse2 = True

                show_message(
                    "FUSE 2 INSTALLED.",
                    100
                )

            else:

                show_message(
                    "NOTHING HAPPENS.",
                    80
                )

            register_player_activity()

            return

        # ----------------------------------------------------
        # FUSE 3
        # ----------------------------------------------------

        if interactable(fuse_rects[2]):

            if (
                basement_power
                and not fuse3
            ):

                fuse3 = True

                show_message(
                    "FUSE 3 INSTALLED.",
                    100
                )

            else:

                show_message(
                    "NOTHING HAPPENS.",
                    80
                )

            register_player_activity()

            return

        # ----------------------------------------------------
        # SECRET DOOR
        # ----------------------------------------------------

        if interactable(secret_door):

            if puzzle_complete:

                room = "secret"

                player.x = 70
                player.y = 300

                show_message(
                    "THE SECRET ROOM.",
                    140
                )

            else:

                show_message(
                    "THE DOOR WILL NOT OPEN.",
                    100
                )

            register_player_activity()

            return

        # ----------------------------------------------------
        # BASEMENT EXIT
        # ----------------------------------------------------

        if interactable(basement_exit):

            if (
                watched_vhs3
                and puzzle_complete
            ):

                choose_basement_ending()

            elif not watched_vhs3:

                show_message(
                    "THE RECORDING IS INCOMPLETE.",
                    120
                )

            elif not puzzle_complete:

                show_message(
                    "THE EXIT HAS NO POWER.",
                    120
                )

            register_player_activity()

            return

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
                "VHS TAPE 4 FOUND.",
                120
            )

            register_player_activity()

            return

        if interactable(secret_tv):

            if (
                has_vhs4
                and not watched_vhs4
            ):

                watched_vhs4 = True

                fear_level = min(
                    100,
                    fear_level + 20
                )

                tv_glitch_timer = 100

                show_message(
                    "YOU CAME BACK.",
                    180
                )

                if not creature_visible:

                    spawn_creature(
                        player.centerx + 170,
                        player.centery
                    )

                register_player_activity()

                return

            if (
                has_vhs5
                and not watched_vhs5
            ):

                watched_vhs5 = True

                fear_level = 100

                tv_glitch_timer = 140

                show_message(
                    "THIS WAS NEVER FOR YOU.",
                    180
                )

                if not creature_visible:

                    spawn_creature(
                        player.centerx + 160,
                        player.centery
                    )

                register_player_activity()

                return

        # ----------------------------------------------------
        # VHS 5
        # ----------------------------------------------------

        if (
            not has_vhs5
            and interactable(vhs5)
        ):

            if watched_vhs4:

                has_vhs5 = True

                show_message(
                    "VHS TAPE 5 FOUND.",
                    150
                )

            else:

                show_message(
                    "YOU DON'T KNOW WHAT THIS IS.",
                    120
                )

            register_player_activity()

            return

        # ----------------------------------------------------
        # SECRET EXIT
        # ----------------------------------------------------

        if interactable(secret_exit):

            # Extremely difficult hidden ending.
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
                    "YOU ARE NOT READY TO LEAVE.",
                    120
                )

            register_player_activity()

            return


# ============================================================
# RESET
# ============================================================

def reset_game():

    global room

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

    global player

    global creature_visible
    global creature_x
    global creature_y
    global creature_state
    global creature_timer
    global creature_chase_timer

    global afk_timer
    global afk_stage
    global afk_hunt_active
    global afk_hunt_timer

    global last_player_x
    global last_player_y
    global player_activity

    global flash_timer
    global screen_shake

    global message
    global message_timer

    global fear_level

    global health
    global health_flash_timer
    global health_shake_timer

    global battery
    global flashlight_on
    global battery_timer
    global flash_flicker_timer

    global random_event_timer
    global tv_glitch_timer
    global heartbeat_timer

    global shadow_timer
    global shadow_visible

    global house_event_timer

    global look_away_timer
    global look_event_count

    room = "hall"

    player.x = 480
    player.y = 520

    ending = False

    normal_ending = False
    bad_ending = False
    loop_ending = False
    secret_ending = False
    true_ending = False
    memory_ending = False
    vhs5_ending = False
    mary_shaw_ending = False
    death_ending = False

    creature_visible = False

    creature_x = 800
    creature_y = 300

    creature_state = "idle"

    creature_timer = 0
    creature_chase_timer = 0

    # --------------------------------------------------------
    # AFK RESET
    # --------------------------------------------------------

    afk_timer = 0
    afk_stage = 0

    afk_hunt_active = False
    afk_hunt_timer = 0

    last_player_x = player.x
    last_player_y = player.y

    player_activity = False

    # --------------------------------------------------------
    # HORROR RESET
    # --------------------------------------------------------

    flash_timer = 0
    screen_shake = 0

    message = ""
    message_timer = 0

    fear_level = min(
        100,
        10 + completed_runs * 5
    )

    # --------------------------------------------------------
    # HEALTH RESET
    # --------------------------------------------------------

    health = MAX_HEALTH

    health_flash_timer = 0
    health_shake_timer = 0

    # --------------------------------------------------------
    # FLASHLIGHT RESET
    # --------------------------------------------------------

    battery = 100
    flashlight_on = True

    battery_timer = 0
    flash_flicker_timer = 0

    # --------------------------------------------------------
    # TIMER RESET
    # --------------------------------------------------------

    random_event_timer = 0
    tv_glitch_timer = 0
    heartbeat_timer = 0

    shadow_timer = 0
    shadow_visible = False

    house_event_timer = 0

    look_away_timer = 0
    look_event_count = 0

    reset_items()

    show_message(
        "THE HOUSE REMEMBERS.",
        180
    )


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

            # ------------------------------------------------
            # ESCAPE
            # ------------------------------------------------

            if event.key == pygame.K_ESCAPE:

                running = False

                continue

            # ------------------------------------------------
            # ENDING RESTART
            # ------------------------------------------------

            if ending:

                if event.key == pygame.K_r:

                    reset_game()

                continue

            # ------------------------------------------------
            # FLASHLIGHT
            # ------------------------------------------------

            if event.key == pygame.K_f:

                if battery > 0:

                    flashlight_on = not flashlight_on

                    register_player_activity()

            # ------------------------------------------------
            # INTERACTION
            # ------------------------------------------------

            elif event.key == pygame.K_e:

                handle_interaction()

    # ========================================================
    # GAME UPDATE
    # ========================================================

    if not ending:

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

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

        # Normalize diagonal movement.
        if dx != 0 and dy != 0:

            factor = 0.7071

            dx = int(
                dx * factor
            )

            dy = int(
                dy * factor
            )

        # ----------------------------------------------------
        # PLAYER MOVEMENT
        # ----------------------------------------------------

        old_x = player.x
        old_y = player.y

        player.x += dx

        # Bedroom bed collision.
        if (
            room == "bedroom"
            and player.colliderect(bed)
        ):

            player.x = old_x

        player.y += dy

        if (
            room == "bedroom"
            and player.colliderect(bed)
        ):

            player.y = old_y

        # ----------------------------------------------------
        # ROOM BOUNDS
        # ----------------------------------------------------

        player.left = max(
            ROOM_BOUNDS.left + 5,
            player.left
        )

        player.right = min(
            ROOM_BOUNDS.right - 5,
            player.right
        )

        player.top = max(
            ROOM_BOUNDS.top + 5,
            player.top
        )

        player.bottom = min(
            ROOM_BOUNDS.bottom - 5,
            player.bottom
        )

        # ----------------------------------------------------
        # AFK SYSTEM
        # ----------------------------------------------------

        update_afk_system()

        # ----------------------------------------------------
        # CREATURE
        # ----------------------------------------------------

        update_creature()

        # ----------------------------------------------------
        # VHS 2 LOOK-AWAY SYSTEM
        # ----------------------------------------------------

        if watched_vhs2:

            look_away_timer += 1

            if (
                look_away_timer >= 700
                and look_event_count == 0
            ):

                look_event_count = 1

                if not creature_visible:

                    spawn_creature(
                        player.centerx + 220,
                        player.centery
                    )

                show_message(
                    "DON'T LOOK AWAY.",
                    130
                )

            elif (
                look_away_timer >= 1400
                and look_event_count == 1
            ):

                look_event_count = 2

                if not creature_visible:

                    spawn_creature(
                        player.centerx - 220,
                        player.centery
                    )

                show_message(
                    "IT MOVED.",
                    130
                )

        # ----------------------------------------------------
        # FLASHLIGHT BATTERY
        # ----------------------------------------------------

        if (
            flashlight_on
            and battery > 0
        ):

            battery_timer += 1

            if battery_timer >= 120:

                battery_timer = 0

                battery -= 1

                battery = max(
                    0,
                    battery
                )

        if battery <= 0:

            flashlight_on = False

        # ----------------------------------------------------
        # LOW BATTERY FLICKER
        # ----------------------------------------------------

        if (
            battery <= 25
            and flashlight_on
        ):

            if random.randint(
                1,
                180
            ) == 1:

                flash_flicker_timer = random.randint(
                    3,
                    10
                )

        if flash_flicker_timer > 0:

            flash_flicker_timer -= 1

        # ----------------------------------------------------
        # HORROR SYSTEMS
        # ----------------------------------------------------

        random_horror_event()
        shadow_event()
        house_reaction()

        # ----------------------------------------------------
        # FUSE PUZZLE
        # ----------------------------------------------------

        if (
            fuse1
            and fuse2
            and fuse3
            and not puzzle_complete
        ):

            puzzle_complete = True

            show_message(
                "THE EXIT POWER IS RESTORED.",
                150
            )

            fear_level = min(
                100,
                fear_level + 8
            )

        # ----------------------------------------------------
        # FEAR
        # ----------------------------------------------------

        if fear_level > 0:

            if random.randint(
                1,
                300
            ) == 1:

                fear_level -= 1

        fear_level = max(
            0,
            min(100, fear_level)
        )

        # ----------------------------------------------------
        # HEARTBEAT
        # ----------------------------------------------------

        if fear_level >= 70:

            if heartbeat_timer <= 0:

                heartbeat_timer = max(
                    35,
                    100 - fear_level
                )

            else:

                heartbeat_timer -= 1

        else:

            heartbeat_timer = 0

        # ----------------------------------------------------
        # TIMERS
        # ----------------------------------------------------

        if message_timer > 0:
            message_timer -= 1

        if tv_glitch_timer > 0:
            tv_glitch_timer -= 1

        if flash_timer > 0:
            flash_timer -= 1

        if screen_shake > 0:
            screen_shake -= 1

        if health_flash_timer > 0:
            health_flash_timer -= 1

        if health_shake_timer > 0:
            health_shake_timer -= 1

        # ----------------------------------------------------
        # SHADOW FADE
        # ----------------------------------------------------

        if shadow_visible:

            if random.randint(
                1,
                50
            ) == 1:

                shadow_visible = False

    # ========================================================
    # DRAW
    # ========================================================

    if ending:

        show_ending()

    else:

        draw_room()

        # ----------------------------------------------------
        # TV GLITCH
        # ----------------------------------------------------

        if tv_glitch_timer > 0:

            glitch = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            glitch.fill(
                (100, 100, 100, 30)
            )

            for _ in range(35):

                y = random.randint(
                    0,
                    HEIGHT - 1
                )

                pygame.draw.line(
                    glitch,
                    (180, 180, 180, 45),
                    (0, y),
                    (WIDTH, y),
                    random.randint(1, 3)
                )

            screen.blit(
                glitch,
                (0, 0)
            )

        # ----------------------------------------------------
        # FLASHLIGHT
        # ----------------------------------------------------

        draw_flashlight()

        # ----------------------------------------------------
        # HEALTH DAMAGE FLASH
        # ----------------------------------------------------

        if health_flash_timer > 0:

            alpha = min(
                120,
                health_flash_timer * 5
            )

            red_overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            red_overlay.fill(
                (180, 0, 0, alpha)
            )

            screen.blit(
                red_overlay,
                (0, 0)
            )

        # ----------------------------------------------------
        # SCREEN SHAKE
        # ----------------------------------------------------

        if screen_shake > 0:

            shake_x = random.randint(
                -screen_shake,
                screen_shake
            )

            shake_y = random.randint(
                -screen_shake,
                screen_shake
            )

            shake_surface = screen.copy()

            screen.fill(BLACK)

            screen.blit(
                shake_surface,
                (
                    shake_x,
                    shake_y
                )
            )

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        draw_ui()
        draw_message()

    pygame.display.flip()

# ============================================================
# EXIT
# ============================================================

pygame.quit()
sys.exit()
