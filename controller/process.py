import configs.config as config
import pygame
import sys

pygame.init()

class Process:
    def __init__(self):
        self.clock = pygame.time.Clock()
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

    def _update(self, dt: float, mouse_pos):
        state = self.session.state

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
        if state != config.P1_SELECT and self.session.state == config.P1_SELECT:
            self.p1_screen.reset(self.session.moves_this_round)