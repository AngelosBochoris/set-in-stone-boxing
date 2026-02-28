"""
logic/main.py
─────────────────────────────────────────────────────
Responsibilities:
  - Networking: send this client's moves to the server,
                receive the opponent's moves from the server.
  - Resolution: resolve both move sequences locally into
                a list of per-step results.
  - Delivery:   serve those results to the Game layer
                one step at a time via next_step().

The server is a dumb move exchange — it does NOT resolve
combat. It only pairs two clients and relays their moves.

Public API (the only surface Game touches):
  submit_moves(moves)  → None
  poll_result()        → None | dict
  next_step()          → None | dict

No pygame imports. No rendering logic.
─────────────────────────────────────────────────────
"""

from logic.resolver import resolve_moves  # local resolution engine


class Logic:
    def __init__(self):
        # TODO: open network connection / session here
        self._my_moves:   list[str]   = []
        self._steps:      list[dict]  = []
        self._step_index: int         = 0
        self._result:     dict | None = None

    # ─────────────────────────────────────────────────
    #  Step 1 — called by Game when P1 locks their moves
    # ─────────────────────────────────────────────────

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
        """
        Check whether the opponent's moves have arrived from the server.
        If they have, resolve the round locally and cache the result.

        Returns:
            None  — still waiting for opponent's moves.
            dict  — full resolution result (see shape below) once ready.

        Internally this method should:
            1. Check the network buffer (non-blocking recv / async check).
            2. If opponent moves have arrived, call resolve_moves() locally.
            3. Cache and return the result dict.

        Result shape:
            {
                "steps": [
                    {
                        "p1_move":      str,   # this client's move at step i
                        "p2_move":      str,   # opponent's move at step i
                        "damage_to_p1": int,
                        "damage_to_p2": int,
                    },
                    ...                        # one entry per move step
                ],
                "final_p1_health": int,
                "final_p2_health": int,
            }
        """
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