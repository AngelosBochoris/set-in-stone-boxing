def get_result_of_moves(p1_moves: list[str], p2_moves: list[str], p1_health: int = 100, p2_health: int = 100, ) -> dict:
    length = max(len(p1_moves), len(p2_moves))
    p1_padded = p1_moves + ["Idle"] * (length - len(p1_moves))
    p2_padded = p2_moves + ["Idle"] * (length - len(p2_moves))

    steps = []
    for m1, m2 in zip(p1_padded, p2_padded):
        d1, d2 = _resolve_step(m1, m2)
        p1_health = max(0, p1_health - d1)
        p2_health = max(0, p2_health - d2)
        steps.append({
            "p1_move":      m1,
            "p2_move":      m2,
            "damage_to_p1": d1,
            "damage_to_p2": d2,
        })
    return {
        "steps":            steps,
        "final_p1_health":  p1_health,
        "final_p2_health":  p2_health,
    }


# ─────────────────────────────────────────────────────
#  Per-step resolution
#
#  TODO: replace this placeholder table with your real
#        combat rules (rock-paper-scissors style matrix,
#        stat-based formula, etc.)
# ─────────────────────────────────────────────────────

# Outcome table: (p1_move, p2_move) → (damage_to_p1, damage_to_p2)
# Extend this as your combat design evolves.
L=5
M=10
H=15
_OUTCOME_TABLE: dict[tuple[str, str], tuple[int, int]] = {
    # Attack Left
    ("Attack Left", "Attack Left"):   (M, M),
    ("Attack Left", "Defend Left"):  (0, M),
    ("Attack Left", "Counter Left"):   (0, H),
    ("Attack Left", "Attack Right"):  (L, L),
    ("Attack Left", "Defend Right"):   (L, 0),
    ("Attack Left", "Counter Right"):  (H, 0),
    ("Attack Left", "Idle"):  (0, M),

    # Defend Left
    ("Defend Left", "Attack Left"): (M, 0),
    ("Defend Left", "Defend Left"): (0, 0),
    ("Defend Left", "Counter Left"): (0, L),
    ("Defend Left", "Attack Right"): (0, L),
    ("Defend Left", "Defend Right"): (0, 0),
    ("Defend Left", "Counter Right"): (M, 0),
    ("Defend Left", "Idle"): (0, 0),

    # Counter Left
    ("Counter Left", "Attack Left"): (H, 0),
    ("Counter Left", "Defend Left"): (L, 0),
    ("Counter Left", "Counter Left"): (H, H),
    ("Counter Left", "Attack Right"): (0, H),
    ("Counter Left", "Defend Right"): (0, M),
    ("Counter Left", "Counter Right"): (L, L),
    ("Counter Left", "Idle"): (0, M),

    # Attack Right
    ("Attack Right", "Attack Left"): (L, L),
    ("Attack Right", "Defend Left"): (L, 0),
    ("Attack Right", "Counter Left"): (H, 0),
    ("Attack Right", "Attack Right"): (M, M),
    ("Attack Right", "Defend Right"): (0, M),
    ("Attack Right", "Counter Right"): (0, H),
    ("Attack Right", "Idle"): (0, M),

    # Defend Right
    ("Defend Right", "Attack Left"): (0, L),
    ("Defend Right", "Defend Left"): (0, 0),
    ("Defend Right", "Counter Left"): (M, 0),
    ("Defend Right", "Attack Right"): (M, 0),
    ("Defend Right", "Defend Right"): (0, 0),
    ("Defend Right", "Counter Right"): (0, L),
    ("Defend Right", "Idle"): (0, 0),

    # Counter Right
    ("Counter Right", "Attack Left"): (0, H),
    ("Counter Right", "Defend Left"): (0, M),
    ("Counter Right", "Counter Left"): (L, L),
    ("Counter Right", "Attack Right"): (H, 0),
    ("Counter Right", "Defend Right"): (L, 0),
    ("Counter Right", "Counter Right"): (H, H),
    ("Counter Right", "Idle"): (0, M),

    # Idle
    ("Idle", "Attack Left"): (M, 0),
    ("Idle", "Defend Left"): (0, 0),
    ("Idle", "Counter Left"): (M, 0),
    ("Idle", "Attack Right"): (M, 0),
    ("Idle", "Defend Right"): (0, 0),
    ("Idle", "Counter Right"): (M, 0),
    ("Idle", "Idle"): (0, 0),
}

_DEFAULT_OUTCOME: tuple[int, int] = (0, 0)  # fallback for unlisted pairs


def _resolve_step(p1_move: str, p2_move: str) -> tuple[int, int]:
    """
    Return (damage_to_p1, damage_to_p2) for a single move pair.
    Looks up the outcome table; falls back to (0, 0) for missing entries.
    """
    return _OUTCOME_TABLE.get((p1_move, p2_move), _DEFAULT_OUTCOME)