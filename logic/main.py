from network.interface import Network


class Logic:
    def __init__(self):
        self._my_moves: list[str] = []
        self._steps: list[dict] = []
        self._step_index: int = 0
        self._result: dict | None = None

        self._connected = False
        self._connecting = False
        self._connection = None

    def start_connection(self):
        if self._connecting:
            return
        self._connecting = True
        self._connection = Network("10.252.95.244")  # your networking wrapper

    def is_connected(self) -> bool:
        if not self._connecting:
            return False
        if self._connected:
            return True

        # non-blocking check
        if self._connection and self._connection.client.ready:
            self._connected = True

        return self._connected

    def submit_moves(self, moves: list[str]) -> None:
        """
        Store moves locally and send them to the server.
        Non-blocking — do NOT wait for a response here.

        The server's only job is to forward these to the
        opponent and send the opponent's moves back.

        Args:
            moves: e.g. ["Attack Left", "Defend Right", "Counter Left"]
        """
        self._my_moves = moves
        # TODO: serialise and send moves over the network, e.g.:
        #   self._socket.sendall(json.dumps({"moves": moves}).encode())

    # ─────────────────────────────────────────────────
    #  Step 2 — polled every frame while in WAITING state
    # ─────────────────────────────────────────────────

    def poll_result(self) -> dict | None:
        if self._result is not None:
            return self._result  # already resolved, return cached result

        # TODO: non-blocking check for opponent's moves, e.g.:
        #   opponent_moves = self._try_receive_opponent_moves()
        #   if opponent_moves is None:
        #       return None

        # Once opponent moves are received, resolve locally:
        #   self._result = resolve_moves(self._my_moves, opponent_moves)
        #   self._steps  = self._result["steps"]
        #   return self._result

        return None  # still waiting

    # ─────────────────────────────────────────────────
    #  Step 3 — called once per STEP_DELAY tick in RESOLVE
    # ─────────────────────────────────────────────────

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
