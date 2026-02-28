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
_OUTCOME_TABLE: dict[tuple[str, str], tuple[int, int]] = {
    # Attack vs Attack  — both take damage (trade)
    ("Attack Left",  "Attack Left"):   (10, 10),
    ("Attack Left",  "Attack Right"):  (10, 10),
    ("Attack Right", "Attack Left"):   (10, 10),
    ("Attack Right", "Attack Right"):  (10, 10),

    # Attack vs Defend (same side) — blocked, no damage
    ("Attack Left",  "Defend Left"):   ( 0,  0),
    ("Attack Right", "Defend Right"):  ( 0,  0),

    # Attack vs Defend (opposite side) — attack lands
    ("Attack Left",  "Defend Right"):  ( 0, 15),
    ("Attack Right", "Defend Left"):   ( 0, 15),

    # Attack vs Counter (same side) — counter wins
    ("Attack Left",  "Counter Left"):  (20,  0),
    ("Attack Right", "Counter Right"): (20,  0),

    # Attack vs Counter (opposite side) — attack lands
    ("Attack Left",  "Counter Right"): ( 0, 15),
    ("Attack Right", "Counter Left"):  ( 0, 15),

    # Defend vs anything — defender takes no damage
    ("Defend Left",  "Attack Left"):   ( 0,  0),
    ("Defend Left",  "Attack Right"):  (15,  0),
    ("Defend Right", "Attack Left"):   (15,  0),
    ("Defend Right", "Attack Right"):  ( 0,  0),

    # Counter vs Attack — mirror of Attack vs Counter
    ("Counter Left",  "Attack Left"):  ( 0, 20),
    ("Counter Right", "Attack Right"): ( 0, 20),
    ("Counter Left",  "Attack Right"): (15,  0),
    ("Counter Right", "Attack Left"):  (15,  0),

    # Idle
    ("Idle", "Idle"):         (0, 0),
}

_DEFAULT_OUTCOME: tuple[int, int] = (0, 0)  # fallback for unlisted pairs


def _resolve_step(p1_move: str, p2_move: str) -> tuple[int, int]:
    """
    Return (damage_to_p1, damage_to_p2) for a single move pair.
    Looks up the outcome table; falls back to (0, 0) for missing entries.
    """
    return _OUTCOME_TABLE.get((p1_move, p2_move), _DEFAULT_OUTCOME)