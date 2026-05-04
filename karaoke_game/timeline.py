"""
Timeline integration for the karaoke game.

Given a list of (start, duration, pitch) notes, this class
returns the expected note at the current playback time.
"""

import time


class SongTimeline:
    def __init__(self, notes):
        """Initialize the song timeline with a list of notes."""
        self.notes = notes
        self.start_time = None
        self.paused = True
        self.pause_start = None
        self.total_paused = 0.0

    def start(self):
        """Start the song timeline."""
        self.start_time = time.time()
        self.paused = True
        self.pause_start = time.time()
        self.total_paused = 0.0

    def pause(self):
        """Pause the song timeline."""
        if not self.paused:
            self.paused = True
            self.pause_start = time.time()

    def resume(self):
        """Resume the song timeline."""
        if self.paused:
            self.paused = False
            self.total_paused += time.time() - self.pause_start

    def get_current_time(self):
        """Get the current playback time in seconds, accounting for pauses."""
        if self.start_time is None:
            return 0.0
        if self.paused:
            return self.pause_start - self.start_time - self.total_paused
        return time.time() - self.start_time - self.total_paused

    def get_current_note(self):
        """Return the expected note (pitch, start, end) at the current time, or None if no note."""
        t = self.get_current_time()
        for start, dur, midi in self.notes:
            if start <= t <= start + dur:
                return midi, start, start + dur
        return None
