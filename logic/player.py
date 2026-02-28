"""
logic/player.py
─────────────────────────────────────────────────────
Player model.

Owns identity, health, and the move sequence chosen
for the current round. No pygame. No rendering.
─────────────────────────────────────────────────────
"""


class Player:
    def __init__(self, name: str, max_health: int = 100):
        self.name: str = name
        self.max_health: int = max_health
        self.health: int = max_health
        self.moves: list[str] = []  # move sequence for the current round

    # ── move management ───────────────────────────

    def set_moves(self, moves: list[str]) -> None:
        self.moves = list(moves)

    def clear_moves(self) -> None:
        self.moves = []

    # ── health management ─────────────────────────

    def apply_damage(self, amount: int) -> None:
        self.health = max(0, self.health - amount)

    def reset_health(self) -> None:
        self.health = self.max_health

    # ── convenience queries ───────────────────────

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def health_fraction(self) -> float:
        """0.0 – 1.0, useful for health bar rendering."""
        return self.health / self.max_health

    def __repr__(self) -> str:
        return f"Player({self.name!r}, health={self.health}/{self.max_health})"
