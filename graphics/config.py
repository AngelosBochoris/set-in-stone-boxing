import pygame

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────

WINDOW_W, WINDOW_H = 1000, 600
FPS = 60
TITLE = "Boxing Game"

# Game states
MAIN_MENU = "MAIN_MENU"
P1_SELECT = "P1_SELECT"
WAITING   = "WAITING"       # waiting for server result
RESOLVE   = "RESOLVE"
GAME_OVER = "GAME_OVER"
# P2_SELECT removed — this client is single-player online

# Selection rules
MIN_MOVES        = 2
MAX_MOVES        = 6
SELECTION_TIME   = 10.0     # seconds
RESOLVE_DURATION = 2.0      # seconds

# Step-by-step resolution
STEP_DELAY = 0.8            # seconds between each move step reveal

# Colours
C_BG         = (15,  15,  25)
C_PANEL      = (28,  28,  45)
C_ACCENT1    = (220, 80,  60)
C_ACCENT2    = (60,  130, 220)
C_TEXT       = (230, 230, 230)
C_SUBTEXT    = (150, 150, 170)
C_BTN_IDLE   = (40,  40,  65)
C_BTN_HOVER  = (60,  60,  95)
C_BTN_PRESS  = (90,  50,  130)
C_BTN_LOCKED = (55,  55,  55)
C_TIMER_OK   = (100, 220, 120)
C_TIMER_WARN = (230, 180,  50)
C_TIMER_CRIT = (230,  60,  60)
C_HEALTH_BAR = (60,  200,  80)
C_HEALTH_LOW = (220,  60,  60)

# Move definitions: (label, keyboard key constant, key name shown on button)
MOVE_DEFS = [
    ("Attack Left",   pygame.K_q, "Q"),
    ("Attack Right",  pygame.K_w, "W"),
    ("Defend Left",   pygame.K_a, "A"),
    ("Defend Right",  pygame.K_s, "S"),
    ("Counter Left",  pygame.K_z, "Z"),
    ("Counter Right", pygame.K_x, "X"),
]