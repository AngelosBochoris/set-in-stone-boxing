from typing import *
from enum import Enum
from utils import get_action_matrix


class Player:
    def __init__(self, p_id: int):
        self.id = p_id
        self.health = 100
        # TODO

    pass


class Move(Enum):
    ATT_L = 0
    ATT_R = 1
    DEF_L = 2
    DEF_R = 3
    DOG_L = 4
    DOG_R = 5


class Game:
    action_matrix: Dict[Tuple[Move, Move], Any] = get_action_matrix()

    def __init__(self, p1_id: int, p2_id: int, inform_state_update: Callable[[Dict[int, Player]], None]):
        self.players = {p1_id: Player(p1_id), p2_id: Player(p2_id)}
        self.inform_state_update = inform_state_update

    def play_move(self, p1_move: Move, p2_move: Move):
        actions = self.action_matrix[p1_move, p2_move]
        # TODO: play actions

        self.inform_state_update(self.players)
        pass

    def play_moves(self, p1_moves: List[Move], p2_moves: List[Move]) -> None:
        assert len(p1_moves) == len(p2_moves)
        for p1_move, p2_move in zip(p1_moves, p2_moves):
            self.play_move(p1_move, p2_move)
