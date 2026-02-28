from model.resolver import get_result_of_moves

class Logic:
    def __init__(self, network):
        self._my_moves: list[str] = []
        self._steps: list[dict] = []
        self._step_index: int = 0
        self._result: dict | None = None

        self._connected = False
        self._connecting = False
        self._connection = network



    def submit_moves(self, moves: list[str]) -> dict | None:
        """
        Store moves locally and send them to the server.
        Non-blocking — do NOT wait for a response here.

        The server's only job is to forward these to the
        opponent and send the opponent's moves back.

        Args:
            moves: e.g. ["Attack Left", "Defend Right", "Counter Left"]
        """
        self._my_moves = moves
        print("submit_moves:",moves)
        string_of_moves = ""
        if len(moves) == 0:
            moves = ["Idle", "Idle"]
        for move in moves:
            string_of_moves += move + ","
        string_of_moves = string_of_moves[:-1]
        opponent_moves = self._connection.send_move(string_of_moves)
        opponent_moves_list = opponent_moves.split(",")

        if self._connection.game_over:
            return None
        else:
            print(opponent_moves_list)
            self._result = get_result_of_moves(self._my_moves, opponent_moves_list)
            self._steps = self._result["steps"]
            self._step_index = 0
            return self._result

    def next_step(self) -> dict | None:
        """
        Pop and return the next resolved step for the UI to display.

        Returns:
            dict  — the next step if one is available.
            None  — all steps have been consumed; round is over.

        Each step dict:
            {
                "p1_move":      str,
                "p2_move":      str,
                "damage_to_p1": int,
                "damage_to_p2": int,
            }
        """
        if self._step_index >= len(self._steps):
            return None
        step = self._steps[self._step_index]
        self._step_index += 1
        return step
