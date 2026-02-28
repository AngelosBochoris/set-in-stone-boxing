import random
import configs.config as config
from controller.connection import Connection as Connection
from model.player import Player
from model.main import Logic


class Battle:
    def __init__(self):
        self.max_rounds: int = 3
        self.battle_state: str = config.MAIN_MENU
        self.round_number: int = 1
        self.player: Player = Player("You")
        self.opponent: Player = Player("Opponent")
        self.logic: Logic = Logic()
        self._steps: list[dict] = []
        self._step_index: int = 0
        self._step_timer: float = 0.0
        self.current_step: dict | None = None

        self.connection = None

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
        """None if game's not over"""
        if self.battle_state != config.GAME_OVER:
            return None
        if self.player.health > self.opponent.health:
            return "player"
        if self.opponent.health > self.player.health:
            return "opponent"
        return "draw"

    def start_game(self) -> None:
        if self.connection is None:
            self.connection = Connection()

        self.round_number = 1
        self.player.reset_health()
        self.opponent.reset_health()

        # TODO
        self.logic = Logic()

        # TODO
        self.connection.start_connection()

        self._transition(config.CONNECTING)

    def submit_player_moves(self, moves: list[str]) -> None:
        """Store moves on the Player and send them to Logic."""
        self.player.set_moves(moves)
        result = self.logic.submit_moves(moves)
        # self._transition(config.WAITING)
        self._steps = result["steps"]
        self._transition(config.RESOLVE)

    def update(self, dt: float) -> None:
        if self.battle_state == config.WAITING:
            self._update_waiting()

        elif self.battle_state == config.CONNECTING:
            self._update_connecting()

        elif self.battle_state == config.RESOLVE:
            self._step_timer -= dt
            if self._step_timer <= 0:
                self._advance_step()

    def _update_waiting(self) -> None:
        result = self.logic.poll_result()
        if result is None:
            return

        self.opponent.set_moves([s["p2_move"] for s in result["steps"]])
        self._steps = result["steps"]
        self._transition(config.RESOLVE)

    def _update_connecting(self) -> None:
        if self.connection.is_connected():
            self._transition(config.P1_SELECT)

    def _advance_step(self) -> None:
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
        self.battle_state = new_state

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

    @property
    def moves_this_round(self) -> int:
        return getattr(self, "_moves_this_round", config.MIN_MOVES)
