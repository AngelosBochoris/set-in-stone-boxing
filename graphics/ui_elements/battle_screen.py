import graphics.config as config
import pygame

# temporary imports
from graphics.ui_elements.button import Button

class SelectionScreen:
    def __init__(self, player_num):
        self.player_num = player_num          # 1 or 2
        self.accent     = config.C_ACCENT1
        self.moves      = []                  # chosen move labels
        self.locked     = False
        self.number_of_moves = 3
        self.time_left  = config.SELECTION_TIME
        self.timer_expired = False

        self._font_title  = pygame.font.SysFont("segoeui", 32, bold=True)
        self._font_timer  = pygame.font.SysFont("segoeui", 48, bold=True)
        self._font_info   = pygame.font.SysFont("segoeui", 20)
        self._font_seq    = pygame.font.SysFont("segoeui", 18)

        self._build_buttons()

    def _build_buttons(self):
        """Lay out 6 move buttons in a 3×2 grid, centred on screen."""
        btn_w, btn_h = 160, 70
        cols, rows   = 3, 2
        gap_x, gap_y = 20, 20

        total_w = cols * btn_w + (cols - 1) * gap_x
        total_h = rows * btn_h + (rows - 1) * gap_y

        start_x = (config.WINDOW_W - total_w) // 2
        start_y = (config.WINDOW_H - total_h) // 2 + 40   # nudge down for header

        self.buttons = []
        for i, (label, key, key_name) in enumerate(config.MOVE_DEFS):
            col = i % cols
            row = i // cols
            x = start_x + col * (btn_w + gap_x)
            y = start_y + row * (btn_h + gap_y)
            self.buttons.append(Button((x, y, btn_w, btn_h), label, key, key_name))

    def reset(self, number_of_moves):
        self.moves     = []
        self.locked    = False
        self.time_left = config.SELECTION_TIME
        self.number_of_moves = number_of_moves
        self.timer_expired = False
        for btn in self.buttons:
            btn.pressed = False
            btn.locked  = False

    def _lock(self):
        self.locked = True
        for btn in self.buttons:
            btn.locked = True

    # ── update ────────────────────────────────

    def update(self, dt):
        # if self.locked:
        #     return
        self.time_left -= dt
        if self.time_left <= 0:
            self.locked = True
            self.timer_expired = True

    # ── event handling ────────────────────────

    def handle_event(self, event, mouse_pos):
        if self.locked:
            return
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                self._on_button(btn)

    def _on_button(self, btn):
        if len(self.moves) < self.number_of_moves:
            self.moves.append(btn.label)
            btn.pressed = True
        if len(self.moves) >= self.number_of_moves:
            self._lock()

    # ── draw ──────────────────────────────────

    def draw(self, surface):
        surface.fill(config.C_BG)
        self._draw_header(surface)
        self._draw_timer(surface)
        for btn in self.buttons:
            btn.draw(surface)
        self._draw_sequence(surface)

    def _draw_header(self, surface):
        label = f"Player {self.player_num}  —  Choose {self.number_of_moves} Moves"
        surf  = self._font_title.render(label, True, self.accent)
        rect  = surf.get_rect(midtop=(config.WINDOW_W // 2, 18))
        surface.blit(surf, rect)

        remaining = self.number_of_moves - len(self.moves)
        sub_text  = "Selection locked!" if self.locked else f"{remaining} move(s) remaining"
        sub_surf  = self._font_info.render(sub_text, True, config.C_SUBTEXT)
        sub_rect  = sub_surf.get_rect(midtop=(config.WINDOW_W // 2, 58))
        surface.blit(sub_surf, sub_rect)

    def _draw_timer(self, surface):
        # Choose colour by urgency
        if self.time_left > 5:
            colour = config.C_TIMER_OK
        elif self.time_left > 2.5:
            colour = config.C_TIMER_WARN
        else:
            colour = config.C_TIMER_CRIT

        timer_str = f"{self.time_left:.1f}s"
        surf = self._font_timer.render(timer_str, True, colour)
        rect = surf.get_rect(topright=(config.WINDOW_W - 30, 15))
        surface.blit(surf, rect)

        label_surf = self._font_info.render("Time left", True, config.C_SUBTEXT)
        label_rect = label_surf.get_rect(topright=(config.WINDOW_W - 30, rect.bottom + 2))
        surface.blit(label_surf, label_rect)

    def _draw_sequence(self, surface):
        if not self.moves:
            return
        seq_text = "  →  ".join(self.moves)
        surf = self._font_seq.render(f"Selected: {seq_text}", True, config.C_TEXT)
        rect = surf.get_rect(midbottom=(config.WINDOW_W // 2, config.WINDOW_H - 20))
        # background pill
        pad = 12
        bg_rect = rect.inflate(pad * 2, pad)
        pygame.draw.rect(surface, config.C_PANEL, bg_rect, border_radius=8)
        surface.blit(surf, rect)
