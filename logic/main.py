from typing import *
from utils import *


class Player:
    def __init__(self, p_id: int):
        self.id = p_id
        self.health = 100
        # TODO

    pass


class GameState:
    action_matrix: Dict[Tuple[Move, Move], Tuple] = get_action_matrix()

    def __init__(self, p1_id: int, p2_id: int, inform_state_update: Callable[[Dict[int,Any]], None]):
        self.players = {p1_id: Player(p1_id), p2_id: Player(p2_id)}
        self.inform_state_update = inform_state_update

    def _play_move(self, p1:int, p1_move: Move, p2:int, p2_move: Move) -> None:
        actions = self.action_matrix[p1_move, p2_move]
        self.inform_state_update({p1:actions[0], p2:actions[1]})

    def play_moves(self, players_moves: Dict[int, List[Move]]) -> None:
        assert len(players_moves) == 2
        with len(next(iter(players_moves.items()))) as l:
            assert all([len(players_moves[i]) == l for i in players_moves])
        p1, p2 = [i for i in players_moves.keys()]

        for p1_move, p2_move in zip(players_moves[p1], players_moves[p2]):
            self._play_move(p1, p1_move, p2, p2_move)

    def process_my_moves(self, p_id: int, p_self_moves: List[Move]):
        x = []
        # --- TODO: call network function for exchange
        # x = ...
        pass
        # ----
        moves = {i: p_self_moves if i == p_id else x for i in self.players}
        self.play_moves(moves)
