import configs.config as config
import pygame
import sys
from enum import Enum

pygame.init()

class Process:
    class Page(Enum):
        MAIN_MENU_PAGE = 0
        BATTLE_MENU_PAGE = 1

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.page = self.Page.MAIN_MENU_PAGE
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

    def _handle_event(self, event, mouse_pos):

        # if state == config.MAIN_MENU:
        if self.page == self.Page.MAIN_MENU_PAGE:
            if self.btn_start.handle_event(event, mouse_pos):
                self.session.start_game()
            if self.btn_quit.handle_event(event, mouse_pos):
                pygame.quit()
                sys.exit()
        else:
            battle_state = self.battle.battle_state
            if battle_state == config.P1_SELECT:
                self.p1_screen.handle_event(event, mouse_pos)

            elif battle_state == config.GAME_OVER:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self.session.battle_state = config.MAIN_MENU

    def _update(self, dt: float, mouse_pos):
        state = self.session.battle_state

        if state == config.MAIN_MENU:
            self.btn_start.hovered = self.btn_start.is_hovered(mouse_pos)
            self.btn_quit.hovered = self.btn_quit.is_hovered(mouse_pos)

        elif state == config.P1_SELECT:
            self.p1_screen.update(dt)
            if self.p1_screen.timer_expired:
                self.session.submit_player_moves(self.p1_screen.moves)
                self.p1_screen.timer_expired = False

        # Delegate all game-state advancement to the session
        self.session.update(dt)

        # Sync SelectionScreen when session transitions back to P1_SELECT
        if state != config.P1_SELECT and self.session.battle_state == config.P1_SELECT:
            self.p1_screen.reset(self.session.moves_this_round)