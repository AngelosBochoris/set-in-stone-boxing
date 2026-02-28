"""
graphics/game.py
─────────────────────────────────────────────────────
Game — display layer only.

Responsibilities:
  - pygame init, window, clock.
  - Own UI widgets (buttons, SelectionScreen).
  - Run the event/update/draw loop.
  - Translate raw input into session calls.
  - Read display data from GameSession and render it.

Does NOT own: game state, round logic, health values,
              step queues, damage, or Player data.
─────────────────────────────────────────────────────
"""

import pygame
import sys

import graphics.config as config
from graphics.ui import Button, SelectionScreen
from control.session import GameSession


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_W, config.WINDOW_H))
        pygame.display.set_caption(config.TITLE)
        self.clock  = pygame.time.Clock()

        self.font_large  = pygame.font.SysFont(None, 52, bold=True)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small  = pygame.font.SysFont(None, 20)
        self.font_tiny   = pygame.font.SysFont(None, 16)

        # ── game state lives here, not in Game ────
        self.session = GameSession()

        # ── UI widgets ────────────────────────────
        self.p1_screen = SelectionScreen(1)
        self._build_menu_buttons()

    # ─────────────────────────────────────────────
    #  Menu buttons
    # ─────────────────────────────────────────────

    def _build_menu_buttons(self):
        bw, bh = 260, 60
        cx = config.WINDOW_W // 2
        self.btn_start = Button(
            (cx - bw // 2, 280, bw, bh), "Start Game",
            key=pygame.K_RETURN, key_name="Enter")
        self.btn_quit = Button(
            (cx - bw // 2, 360, bw, bh), "Quit",
            key=pygame.K_ESCAPE, key_name="Esc")

    # ─────────────────────────────────────────────
    #  Main loop
    # ─────────────────────────────────────────────

    def run(self):
        while True:
            dt = self.clock.tick(config.FPS) / 1000.0
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_event(event, mouse_pos)

            self._update(dt, mouse_pos)
            self._draw()
            pygame.display.flip()

    # ─────────────────────────────────────────────
    #  Event handling — translates input → session
    # ─────────────────────────────────────────────

    def _handle_event(self, event, mouse_pos):
        state = self.session.state

        if state == config.MAIN_MENU:
            if self.btn_start.handle_event(event, mouse_pos):
                self.session.start_game()
            if self.btn_quit.handle_event(event, mouse_pos):
                pygame.quit()
                sys.exit()

        elif state == config.P1_SELECT:
            self.p1_screen.handle_event(event, mouse_pos)

        elif state == config.GAME_OVER:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.session.state = config.MAIN_MENU

        # WAITING and RESOLVE: no player input expected.

    # ─────────────────────────────────────────────
    #  Update — drives session + UI widget state
    # ─────────────────────────────────────────────

    def _update(self, dt: float, mouse_pos):
        state = self.session.state

        if state == config.MAIN_MENU:
            self.btn_start.hovered = self.btn_start.is_hovered(mouse_pos)
            self.btn_quit.hovered  = self.btn_quit.is_hovered(mouse_pos)

        elif state == config.P1_SELECT:
            self.p1_screen.update(dt)
            if self.p1_screen.locked:
                self.session.submit_player_moves(self.p1_screen.moves)

        # Delegate all game-state advancement to the session
        self.session.update(dt)

        # Sync SelectionScreen when session transitions back to P1_SELECT
        if state != config.P1_SELECT and self.session.state == config.P1_SELECT:
            self.p1_screen.reset(self.session.moves_this_round)

    # ─────────────────────────────────────────────
    #  Draw — reads session for display data only
    # ─────────────────────────────────────────────

    def _draw(self):
        state = self.session.state
        if state == config.MAIN_MENU:
            self._draw_main_menu()
        elif state == config.P1_SELECT:
            self.p1_screen.draw(self.screen)
        elif state == config.WAITING:
            self._draw_waiting()
        elif state == config.CONNECTING:
            self._draw_connecting()
        elif state == config.RESOLVE:
            self._draw_resolve()
        elif state == config.GAME_OVER:
            self._draw_game_over()

    # ── screen renderers ──────────────────────────

    def _draw_main_menu(self):
        self.screen.fill(config.C_BG)
        title = self.font_large.render("BOXING GAME", True, config.C_ACCENT1)
        self.screen.blit(title, title.get_rect(
            center=(config.WINDOW_W // 2, 180)))
        sub = self.font_medium.render("1v1 Online Multiplayer", True, config.C_SUBTEXT)
        self.screen.blit(sub, sub.get_rect(
            center=(config.WINDOW_W // 2, 235)))
        self.btn_start.draw(self.screen)
        self.btn_quit.draw(self.screen)

    def _draw_waiting(self):
        self.screen.fill(config.C_BG)
        text = self.font_large.render("Waiting for opponent…", True, config.C_TEXT)
        self.screen.blit(text, text.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 - 20)))
        hint = self.font_small.render(
            "Your moves have been sent. Hang tight.", True, config.C_SUBTEXT)
        self.screen.blit(hint, hint.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 + 35)))
        dots = "." * (1 + (pygame.time.get_ticks() // 500) % 3)
        dots_surf = self.font_medium.render(dots, True, config.C_SUBTEXT)
        self.screen.blit(dots_surf, dots_surf.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 + 75)))

    def _draw_connecting(self):
        self.screen.fill(config.C_BG)
        text = self.font_large.render("Waiting for opponent to connect…", True, config.C_TEXT)
        self.screen.blit(text, text.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 - 20)))
        dots = "." * (1 + (pygame.time.get_ticks() // 500) % 3)
        dots_surf = self.font_medium.render(dots, True, config.C_SUBTEXT)
        self.screen.blit(dots_surf, dots_surf.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 + 75)))

    def _draw_resolve(self):
        self.screen.fill(config.C_BG)
        s = self.session  # read-only alias

        self._draw_health_bars(y_offset=50)

        # Round / step counter
        counter = self.font_small.render(
            f"Round {s.round_number} / {s.max_rounds}  —  "
            f"Step {s.step_index} / {s.total_steps}",
            True, config.C_SUBTEXT)
        self.screen.blit(counter, counter.get_rect(
            midtop=(config.WINDOW_W // 2, 10)))

        # Current step detail
        step = s.current_step
        if step:
            cy = config.WINDOW_H // 2 - 60
            p1_surf = self.font_medium.render(
                f"Your move:  {step.get('p1_move', '—')}", True, config.C_ACCENT1)
            p2_surf = self.font_medium.render(
                f"Opponent:   {step.get('p2_move', '—')}", True, config.C_ACCENT2)
            self.screen.blit(p1_surf, p1_surf.get_rect(
                center=(config.WINDOW_W // 2, cy)))
            self.screen.blit(p2_surf, p2_surf.get_rect(
                center=(config.WINDOW_W // 2, cy + 45)))

            d1 = step.get("damage_to_p1", 0)
            d2 = step.get("damage_to_p2", 0)
            dmg_lines = []
            if d1: dmg_lines.append((f"You took {d1} damage",    config.C_HEALTH_LOW))
            if d2: dmg_lines.append((f"Opponent took {d2} damage", config.C_HEALTH_BAR))
            if not dmg_lines:
                dmg_lines.append(("No damage this step", config.C_SUBTEXT))
            for i, (text, colour) in enumerate(dmg_lines):
                surf = self.font_small.render(text, True, colour)
                self.screen.blit(surf, surf.get_rect(
                    center=(config.WINDOW_W // 2, cy + 105 + i * 28)))
        else:
            loading = self.font_medium.render("Processing…", True, config.C_TEXT)
            self.screen.blit(loading, loading.get_rect(
                center=(config.WINDOW_W // 2, config.WINDOW_H // 2)))

        # Progress bar toward next step
        bar_w, bar_h = 300, 6
        bar_x = (config.WINDOW_W - bar_w) // 2
        bar_y = config.WINDOW_H - 30
        progress = max(0.0, 1.0 - s.step_timer / config.STEP_DELAY)
        pygame.draw.rect(self.screen, config.C_PANEL,
                         (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(self.screen, config.C_ACCENT2,
                         (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=3)

    def _draw_game_over(self):
        self.screen.fill(config.C_BG)
        s = self.session

        result_map = {
            "player":   ("You Win!",  config.C_HEALTH_BAR),
            "opponent": ("You Lose.", config.C_HEALTH_LOW),
            "draw":     ("Draw!",     config.C_TEXT),
        }
        text, colour = result_map.get(s.winner, ("Game Over", config.C_TEXT))

        title = self.font_large.render(text, True, colour)
        self.screen.blit(title, title.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 - 70)))

        self._draw_health_bars(y_offset=config.WINDOW_H // 2 - 10)

        hint = self.font_small.render(
            "Press any key to return to menu", True, config.C_SUBTEXT)
        self.screen.blit(hint, hint.get_rect(
            center=(config.WINDOW_W // 2, config.WINDOW_H // 2 + 80)))

    # ─────────────────────────────────────────────
    #  Shared widget: health bars
    #  Reads from session.player / session.opponent
    # ─────────────────────────────────────────────

    def _draw_health_bars(self, y_offset: int = 50):
        s = self.session
        bar_w, bar_h = 360, 26
        gap     = 40
        start_x = (config.WINDOW_W - (bar_w * 2 + gap)) // 2

        entries = [
            (s.player,   config.C_ACCENT1, start_x),
            (s.opponent, config.C_ACCENT2, start_x + bar_w + gap),
        ]
        for player, accent, x in entries:
            # Background
            pygame.draw.rect(self.screen, config.C_PANEL,
                             (x, y_offset, bar_w, bar_h), border_radius=5)
            # Health fill
            fill_w = int(bar_w * player.health_fraction)
            fill_colour = config.C_HEALTH_BAR if player.health > 30 else config.C_HEALTH_LOW
            if fill_w > 0:
                pygame.draw.rect(self.screen, fill_colour,
                                 (x, y_offset, fill_w, bar_h), border_radius=5)
            # Border
            pygame.draw.rect(self.screen, accent,
                             (x, y_offset, bar_w, bar_h), width=2, border_radius=5)
            # Label
            label = self.font_tiny.render(
                f"{player.name}  {player.health} HP", True, config.C_TEXT)
            self.screen.blit(label, label.get_rect(
                center=(x + bar_w // 2, y_offset + bar_h // 2)))