import graphics.config as config
import pygame

class Button:
    """Reusable button with mouse + keyboard support."""

    def __init__(self, rect, label, key=None, key_name=""):
        self.rect      = pygame.Rect(rect)
        self.label     = label
        self.key       = key        # pygame key constant, or None
        self.key_name  = key_name   # display string for the key hint
        self.hovered   = False
        self.pressed   = False      # selected/active state
        self.locked    = False
        self._font_main = None
        self._font_hint = None

    def _ensure_fonts(self):
        if self._font_main is None:
            self._font_main = pygame.font.SysFont("segoeui", 18, bold=True)
            self._font_hint = pygame.font.SysFont("segoeui", 13)

    # ── state queries ──────────────────────────

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event, mouse_pos):
        """Return True if this button was activated this event."""
        if self.locked:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(mouse_pos)
        if event.type == pygame.KEYDOWN and self.key is not None:
            return event.key == self.key
        return False

    def handle_event(self, event, mouse_pos):
        """Update hover state; return True if button was just activated."""
        if not self.locked:
            self.hovered = self.is_hovered(mouse_pos)
        else:
            self.hovered = False
        return self.is_clicked(event, mouse_pos)

    # ── rendering ─────────────────────────────

    def draw(self, surface):
        self._ensure_fonts()

        if self.locked:
            colour = config.C_BTN_LOCKED
        elif self.pressed:
            colour = config.C_BTN_PRESS
        elif self.hovered:
            colour = config.C_BTN_HOVER
        else:
            colour = config.C_BTN_IDLE

        pygame.draw.rect(surface, colour, self.rect, border_radius=8)
        border_col = (160, 80, 200) if self.pressed else (70, 70, 100)
        pygame.draw.rect(surface, border_col, self.rect, width=2, border_radius=8)

        # Main label
        text_surf = self._font_main.render(self.label, True, config.C_TEXT)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 8))
        surface.blit(text_surf, text_rect)

        # Key hint
        if self.key_name:
            hint_surf = self._font_hint.render(f"[{self.key_name}]", True, config.C_SUBTEXT)
            hint_rect = hint_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 12))
            surface.blit(hint_surf, hint_rect)

