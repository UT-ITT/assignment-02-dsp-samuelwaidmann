"""This module implements a simple pitch smoother using an exponential moving average to stabilize the detected pitch values over time."""


class PitchSmoother:
    def __init__(self, alpha=0.2):
        """Initialize the pitch smoother with a given smoothing factor (alpha)."""
        self.alpha = alpha
        self.value = None

    def update(self, new_value):
        """
        Update the smoothed pitch value with a new detected pitch.

        Arguments:
            new_value: The newly detected MIDI pitch (int or float), or None if no pitch detected.

        Returns:
            The updated smoothed MIDI pitch value.
        """
        if new_value is None:
            return self.value
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value
