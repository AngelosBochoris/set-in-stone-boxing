"""
graphics/animation.py
─────────────────────────────────────────────────────
StepAnimation — a frame-based animation helper that
synchronises exactly to one combat step's duration.

Architecture rules:
  - No imports from logic/, session, or config.
  - No pygame.init() calls.
  - No internal FPS or clock — driven by dt from Game.
  - Pure rendering helper: update(dt) + draw(screen, pos).
─────────────────────────────────────────────────────
"""

import pygame

from graphics import config


class StepAnimation:
    """
    Plays a sequence of frames evenly distributed across one step duration.

    Timing
    ──────
    frame_duration = step_duration / len(frames)

    If step_duration=1.0 and frames=10, each frame shows for 0.1 s.
    The animation completes exactly when the step timer would reach zero.

    Usage (inside Game)
    ───────────────────
        anim = StepAnimation(["hit1.png", "hit2.png", "hit3.png"], step_duration=1.0)

        # When session.step_index changes:
        anim.reset()

        # Every frame:
        anim.update(dt)
        anim.draw(screen, (x, y))
    """

    def __init__(
        self,
        frame_sources: list,        # list[str | pygame.Surface]
        step_duration: float,       # matches config.STEP_DELAY
    ):
        if not frame_sources:
            raise ValueError("StepAnimation requires at least one frame.")
        if step_duration <= 0:
            raise ValueError("step_duration must be > 0.")

        self._frames:         list[pygame.Surface] = self._load_frames(frame_sources)
        self._step_duration:  float = step_duration
        self._frame_duration: float = step_duration / len(self._frames)

        self._timer:       float = 0.0
        self._frame_index: int   = 0
        self._finished:    bool  = False

    # ─────────────────────────────────────────────
    #  Public interface
    # ─────────────────────────────────────────────

    def reset(self) -> None:
        """
        Restart the animation from frame 0.
        Call this every time session.step_index changes.
        """
        self._timer       = 0.0
        self._frame_index = 0
        self._finished    = False

    def update(self, dt: float) -> None:
        """
        Advance the animation by dt seconds.
        Stops permanently on the last frame — does not loop.

        Args:
            dt: Delta time in seconds (from clock.tick / 1000).
        """
        if self._finished:
            return

        self._timer += dt

        # How many frames should have elapsed by now?
        elapsed_frames = int(self._timer / self._frame_duration)
        new_index = min(elapsed_frames, len(self._frames) - 1)

        if new_index != self._frame_index:
            self._frame_index = new_index

        if self._frame_index >= len(self._frames) - 1:
            self._finished = True

    def draw(self, screen: pygame.Surface, position: tuple[int, int]) -> None:
        """
        Blit the current frame at position (top-left corner).
        Safe to call even before update() or after finishing.

        Args:
            screen:   The pygame surface to draw onto.
            position: (x, y) top-left pixel position.
        """
        if not self._frames:
            return
        screen.blit(self._frames[self._frame_index], position)

    def draw_centered(self, screen: pygame.Surface, center: tuple[int, int]) -> None:
        """
        Convenience variant: blit the current frame centred on a point.

        Args:
            screen: The pygame surface to draw onto.
            center: (cx, cy) pixel position for the frame's centre.
        """
        if not self._frames:
            return
        frame = self._frames[self._frame_index]
        rect  = frame.get_rect(center=center)
        screen.blit(frame, rect)

    def is_finished(self) -> bool:
        """
        Returns True once the final frame has been reached.
        The last frame remains visible — the animation does not disappear.
        """
        return self._finished

    # ─────────────────────────────────────────────
    #  Read-only properties (useful for debugging)
    # ─────────────────────────────────────────────

    @property
    def frame_index(self) -> int:
        return self._frame_index

    @property
    def frame_count(self) -> int:
        return len(self._frames)

    @property
    def frame_duration(self) -> float:
        """Seconds each frame is shown."""
        return self._frame_duration

    @property
    def current_frame(self) -> pygame.Surface:
        return self._frames[self._frame_index]

    # ─────────────────────────────────────────────
    #  Internal helpers
    # ─────────────────────────────────────────────

    @staticmethod
    def _load_frames(sources: list) -> list[pygame.Surface]:
        """
        Accept a mixed list of file-path strings and/or pygame.Surface objects.
        Paths are loaded with pygame.image.load() and converted for fast blitting.
        Surfaces are used as-is (caller owns them).
        """
        frames = []
        for src in sources:
            if isinstance(src, str):
                try:
                    surface = pygame.image.load(src).convert_alpha()
                    surface = pygame.transform.scale(surface, config.TARGET_SIZE)
                except FileNotFoundError as exc:
                    raise FileNotFoundError(
                        f"StepAnimation: frame not found — {src}"
                    ) from exc
            elif isinstance(src, pygame.Surface):
                surface = src
            else:
                raise TypeError(
                    f"StepAnimation: expected str or pygame.Surface, got {type(src).__name__}"
                )
            frames.append(surface)
        return frames