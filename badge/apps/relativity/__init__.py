import math
import os
import random
import sys

APP_DIR = "/system/apps/relativity"
os.chdir(APP_DIR)
sys.path.insert(0, APP_DIR)

badge.mode(HIRES | VSYNC)

# Edit these for the name card.
NAME = "Nathan McCorkle"
TITLE = "Senior Software Engineer"
TAGLINE = "The AI platform for legal data intelligence"

ORANGE = color.rgb(239, 95, 17)
BLUE = color.rgb(8, 37, 61)
BLACK = color.rgb(22, 24, 28)
WHITE = color.rgb(252, 253, 254)
GRAY = color.rgb(100, 100, 118)
LIGHT_GRAY = color.rgb(220, 220, 228)

LARGE = font.ziplock
SMALL = font.nope

logo_orange = image.load("assets/logo_orange.png")
r_white = image.load("assets/r_white.png")
rel_orange = image.load("assets/rel_orange.png")
ty_orange = image.load("assets/ty_orange.png")

INTRO, LOGO, CARD = range(3)
CAROUSEL = (INTRO, LOGO, CARD)

FADE_MS = 700
LOGO_HOLD_MS = 1800
DWELL_MS = {LOGO: 60000, CARD: 20000}
EGG_REL_MS = 1800
TILT_PX = 14

index = 0
scene_ms = 0
egg_ms = 0
tilt_x = 0.0
tilt_y = 0.0

random.seed(26)
particles = [
    [random.randrange(320), random.randrange(240), random.randrange(12, 40), random.randrange(1, 4)]
    for _ in range(36)
]


def fill(pen):
    screen.pen = pen
    screen.rectangle(screen.clip)


def centered(text, y, pen):
    width, _ = screen.measure_text(text)
    screen.pen = pen
    screen.text(text, (screen.width - width) / 2, y)


def blit_centered(img, dx=0, dy=0):
    x = (screen.width - img.width) / 2 + dx
    y = (screen.height - img.height) / 2 + dy
    screen.blit(img, vec2(x, y))


def read_tilt(dt):
    global tilt_x, tilt_y
    ax, ay, _az, _gx, _gy, _gz = badge.imu()
    target_x = max(-1.0, min(1.0, ax / 16384))
    target_y = max(-1.0, min(1.0, ay / 16384))
    k = min(1.0, dt * 6)
    tilt_x += (target_x - tilt_x) * k
    tilt_y += (target_y - tilt_y) * k


def go(new_index):
    global index, scene_ms, egg_ms
    index = new_index
    scene_ms = 0
    egg_ms = 0


def build_word_images():
    screen.font = LARGE
    images = []
    for word in TAGLINE.split():
        w, h = screen.measure_text(word)
        img = image(int(w) + 2, int(h) + 2)
        img.font = LARGE
        img.pen = WHITE
        img.text(word, 1, 1)
        images.append(img)
    return images


word_images = build_word_images()
WORD_MS = 350
WORD_MS_PER_CHAR = 40
LAST_WORD_EXTRA_MS = 800
word_ends = []
_t = 0
for _i, _w in enumerate(TAGLINE.split()):
    _t += WORD_MS + WORD_MS_PER_CHAR * len(_w)
    word_ends.append(_t)
word_ends[-1] += LAST_WORD_EXTRA_MS
scroll_ms = word_ends[-1]


def intro():
    if scene_ms < scroll_ms:
        fill(BLACK)
        n = 0
        while scene_ms >= word_ends[n]:
            n += 1
        img = word_images[n]
        scale = min((screen.width - 16) / img.width, (screen.height - 40) / img.height)
        w = img.width * scale
        h = img.height * scale
        screen.pen = ORANGE
        screen.rectangle(rect(0, 8, screen.width, 4))
        screen.rectangle(rect(0, screen.height - 12, screen.width, 4))
        screen.blit(img, rect((screen.width - w) / 2, (screen.height - h) / 2, w, h))
    else:
        t = scene_ms - scroll_ms
        fill(BLUE)
        screen.alpha = int(255 * min(1.0, t / FADE_MS))
        blit_centered(logo_orange)
        screen.alpha = 255
        if t > FADE_MS + LOGO_HOLD_MS:
            go((index + 1) % len(CAROUSEL))


def draw_logo(dt):
    read_tilt(dt)
    fill(BLUE)

    screen.pen = ORANGE
    for p in particles:
        p[1] -= p[2] * dt
        if p[1] < -4:
            p[1] = screen.height + 4
            p[0] = random.randrange(screen.width)
        depth = p[3]
        screen.rectangle(rect(p[0] - tilt_x * depth * 6, p[1] - tilt_y * depth * 6, depth, depth))

    bob = math.sin(badge.ticks / 700) * 4
    blit_centered(logo_orange, -tilt_x * TILT_PX, -tilt_y * TILT_PX + bob)

    screen.font = SMALL
    centered("Hold SELECT", screen.height - 40, GRAY)


def draw_egg():
    fill(BLACK)
    screen.font = LARGE
    if egg_ms < EGG_REL_MS:
        blit_centered(rel_orange, 0, -20)
        centered("Rel: our community's nickname for us", screen.height - 50, WHITE)
    else:
        blit_centered(ty_orange, 0, -20)
        centered("Thank you", screen.height - 50, WHITE)


def draw_card():
    fill(ORANGE)
    screen.blit(r_white, vec2(24, (screen.height - r_white.height) / 2))
    text_x = 24 + r_white.width + 24
    screen.font = LARGE
    screen.pen = WHITE
    screen.text(NAME, text_x, 84)
    screen.font = SMALL
    screen.text(TITLE, text_x, 124)
    screen.pen = BLACK
    screen.text("Relativity", text_x, 148)


def draw_dots():
    active = LIGHT_GRAY if CAROUSEL[index] == CARD else ORANGE
    for i in range(len(CAROUSEL)):
        screen.pen = active if i == index else GRAY
        screen.rectangle(rect(screen.width / 2 - 20 + i * 16, screen.height - 16, 8, 8))


def update():
    global index, scene_ms, egg_ms
    dt = badge.ticks_delta / 1000
    scene_ms += badge.ticks_delta

    if badge.pressed(BUTTON_RIGHT):
        go((index + 1) % len(CAROUSEL))
    elif badge.pressed(BUTTON_LEFT):
        go((index - 1) % len(CAROUSEL))

    # The intro advances itself; the other scenes rotate after a dwell time.
    if CAROUSEL[index] != INTRO and not badge.held(BUTTON_SELECT) and scene_ms > DWELL_MS[CAROUSEL[index]]:
        go((index + 1) % len(CAROUSEL))
    current = CAROUSEL[index]

    if current == INTRO:
        intro()
    elif current == LOGO:
        if badge.held(BUTTON_SELECT):
            egg_ms += badge.ticks_delta
            draw_egg()
            return
        egg_ms = 0
        draw_logo(dt)
    else:
        draw_card()
    draw_dots()


run(update)
