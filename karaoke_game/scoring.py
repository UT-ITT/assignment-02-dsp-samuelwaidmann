"""
Minimal scoring system for karaoke.

Evaluates correctness of sung pitch vs expected pitch.
"""


class ScoringSystem:
    """Simple scoring system for karaoke game."""

    def __init__(self, tolerance_semitones=0.75):
        """Initialize the scoring system."""
        self.tolerance = tolerance_semitones
        self.score = 0
        self.correct_frames = 0
        self.total_frames = 0

    def update(self, expected_midi, sung_midi):
        """
        Update scoring for one audio frame.

        Arguments:
        expected_midi: int or float
        sung_midi: int or float or None

        Returns:
            is_correct (bool)
        """
        self.total_frames += 1

        if sung_midi is None:
            return False

        diff = abs(sung_midi - expected_midi)

        if diff <= self.tolerance:
            self.correct_frames += 1
            self.score += 1
            return True

        return False

    def reset(self):
        """Reset the scoring system for a new game."""
        self.score = 0
        self.correct_frames = 0
        self.total_frames = 0

    def accuracy(self):
        """Calculate accuracy as the percentage of correct frames."""
        if self.total_frames == 0:
            return 0.0
        return self.correct_frames / self.total_frames
