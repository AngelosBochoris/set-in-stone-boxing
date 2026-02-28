"""
logic/session.py
─────────────────────────────────────────────────────
GameSession — owns all game state and drives transitions.

Responsibilities:
  - Track game state (current state string, round number).
  - Own both Player objects.
  - Coordinate with Logic for move submission and result polling.
  - Advance the step-by-step resolve queue.
  - Expose clean, read-only display data to the graphics layer.

The graphics layer (Game) calls:
  session.start_game()
  session.submit_player_moves(moves)
  session.update(dt)               ← called every frame
  session.state                    ← current state string
  session.round_number             ← int
  session.max_rounds               ← int
  session.player                   ← Player (this client)
  session.opponent                 ← Player (remote)
  session.current_step             ← dict | None
  session.step_index               ← int
  session.total_steps              ← int
  session.step_timer               ← float (for progress bar)
  session.winner                   ← "player" | "opponent" | "draw" | None

No pygame. No rendering.
─────────────────────────────────────────────────────
"""

import random
import graphics.config as config
from logic.player import Player
from logic.main import Logic


class GameSession:
    def __init__(self):
        self.max_rounds: int = 3

        # These are reset on start_game()
        self.state: str = config.MAIN_MENU
        self.round_number: int = 1
        self.player: Player = Player("You")
        self.opponent: Player = Player("Opponent")
        self.logic: Logic = Logic()

        # Resolve playback — advanced by update()
        self._steps: list[dict] = []
        self._step_index: int = 0
        self._step_timer: float = 0.0
        self.current_step: dict | None = None

    # ─────────────────────────────────────────────
    #  Read-only display properties
    # ─────────────────────────────────────────────

    @property
    def step_index(self) -> int:
        return self._step_index

    @property
    def total_steps(self) -> int:
        return len(self._steps)

    @property
    def step_timer(self) -> float:
        return self._step_timer

    @property
    def winner(self) -> str | None:
        """Only meaningful in GAME_OVER state."""
        if self.state != config.GAME_OVER:
            return None
        if self.player.health > self.opponent.health:
            return "player"
        if self.opponent.health > self.player.health:
            return "opponent"
        return "draw"

    # ─────────────────────────────────────────────
    #  Game lifecycle
    # ─────────────────────────────────────────────

    def start_game(self) -> None:
        """Reset everything and begin a new game."""
        self.round_number = 1
        self.player.reset_health()
        self.opponent.reset_health()
        self.logic = Logic()
        self._transition(config.CONNECTING)

    # ─────────────────────────────────────────────
    #  Called by Game when the SelectionScreen locks
    # ─────────────────────────────────────────────
    def submit_player_moves(self, moves: list[str]) -> None:
        """Store moves on the Player and send them to Logic."""
        self.player.set_moves(moves)
        self.logic.submit_moves(moves)
        self._transition(config.WAITING)

    # ─────────────────────────────────────────────
    #  Frame update — called every tick by Game
    # ─────────────────────────────────────────────

    def update(self, dt: float) -> None:
        if self.state == config.WAITING:
            self._update_waiting()

        elif self.state == config.CONNECTING:
            self._update_connecting()

        elif self.state == config.RESOLVE:
            self._step_timer -= dt
            if self._step_timer <= 0:
                self._advance_step()

    # ─────────────────────────────────────────────
    #  Internal helpers
    # ─────────────────────────────────────────────

    def _update_waiting(self) -> None:
        result = self.logic.poll_result()
        if result is None:
            return

        # Sync final health from the resolved result
        self.opponent.set_moves([s["p2_move"] for s in result["steps"]])
        self._steps = result["steps"]
        self._transition(config.RESOLVE)

    def _update_connecting(self) -> None:
        while not connection.client.ready:
            continue

        # Sync final health from the resolved result
        self.opponent.set_moves([s["p2_move"] for s in result["steps"]])
        self._steps = result["steps"]
        self._transition(config.RESOLVE)

    def _advance_step(self) -> None:
        """Show the next step, or end the round when steps are exhausted."""
        step = self.logic.next_step()
        if step is not None:
            self.current_step = step
            self._step_index += 1
            # Apply damage to Player objects — single source of truth
            self.player.apply_damage(step.get("damage_to_p1", 0))
            self.opponent.apply_damage(step.get("damage_to_p2", 0))
            self._step_timer = config.STEP_DELAY
        else:
            self.current_step = None
            self._end_round()

    def _end_round(self) -> None:
        if self.round_number < self.max_rounds:
            self.round_number += 1
            self._transition(config.P1_SELECT)
        else:
            self._transition(config.GAME_OVER)

    def _transition(self, new_state: str) -> None:
        self.state = new_state

        if new_state == config.P1_SELECT:
            moves_this_round = random.randint(config.MIN_MOVES, config.MAX_MOVES)
            self._moves_this_round = moves_this_round  # read by Game to reset SelectionScreen
            self.player.clear_moves()
            self.opponent.clear_moves()

        elif new_state == config.RESOLVE:
            self._step_index = 0
            self._step_timer = config.STEP_DELAY
            self.current_step = None
            self._advance_step()  # display first step immediately

    # ─────────────────────────────────────────────
    #  Convenience: how many moves to pick this round
    # ─────────────────────────────────────────────

    @property
    def moves_this_round(self) -> int:
        return getattr(self, "_moves_this_round", config.MIN_MOVES)
