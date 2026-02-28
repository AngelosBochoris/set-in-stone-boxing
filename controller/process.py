import configs.config as config
import pygame
import sys
from enum import Enum

from controller.battle import Battle
from view.display import Display

pygame.init()


class Process:
    class Page(Enum):
        MAIN_MENU_PAGE = 0
        BATTLE_MENU_PAGE = 1

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.battle = Battle()
        self.display = Display()

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

            self.display.draw(self.battle.battle_state)
            pygame.display.flip()

    def _handle_event(self, event, mouse_pos):
        state = self.battle.battle_state
        # if state == config.MAIN_MENU:
        if state == config.MAIN_MENU:
            if self.display.btn_start.handle_event(event, mouse_pos):
                self.battle.start_game()
            if self.display.btn_quit.handle_event(event, mouse_pos):
                pygame.quit()
                sys.exit()
        else:
            if state == config.P1_SELECT:
                self.display.p1_screen.handle_event(event, mouse_pos)

            elif state == config.GAME_OVER:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self.battle.battle_state = config.MAIN_MENU

    def _update(self, dt: float, mouse_pos):
        state = self.battle.battle_state
        d = self.display
        if state == config.MAIN_MENU:
            d.btn_start.hovered = d.btn_start.is_hovered(mouse_pos)
            d.btn_quit.hovered = d.btn_quit.is_hovered(mouse_pos)

        elif state == config.P1_SELECT:
            d.p1_screen.update(dt)
            if d.p1_screen.timer_expired:
                self.battle.submit_player_moves(d.p1_screen.moves)
                d.p1_screen.timer_expired = False

        # Delegate all game-state advancement to the session
        self.battle.update(dt)

        # Sync SelectionScreen when session transitions back to P1_SELECT
        if state != config.P1_SELECT and self.battle.battle_state == config.P1_SELECT:
            d.p1_screen.reset(self.battle.moves_this_round)
