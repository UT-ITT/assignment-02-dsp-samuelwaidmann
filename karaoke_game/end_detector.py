"""This module contains the SongEndDetector class, which determines when the song has finished based on the MIDI notes."""


class SongEndDetector:
    """Detect when the song has finished based on the MIDI notes."""

    def __init__(self, notes):
        """Initialize with a list of (start, duration, midi) notes."""
        self.end_time = max(start + dur for (start, dur, midi) in notes)

    def is_finished(self, t):
        """Return True if the current time t has passed the end of the song."""
        return t >= self.end_time
