"""
Whistle Input Detection and key simulation.

This module implements real-time whistle detection using FFT-based frequency estimation,
slope detection for chirps, and live plotting of frequency and slope.
It simulates key (up and down) presses based on detected chirps.
"""

import numpy as np
import sounddevice as sd
from collections import deque
import time
from pynput.keyboard import Controller, Key
import pyqtgraph as pg

# -----------------------------
# Parameters
# -----------------------------
RATE = 44100  # Hz
CHUNK = 1024  # samples per audio block

WHISTLE_MIN = 300  # Hz
WHISTLE_MAX = 3000  # Hz

AMP_THRESHOLD = 0.02  # ignore quiet frames
SMOOTH_ALPHA = 0.25  # exponential smoothing
WINDOW_SIZE = 30  # window size for slope estimation
SLOPE_THRESHOLD = 400  # Hz/s for chirp detection

MEDIAN_FILTER_SIZE = 5  # for median filter to stabilize frequency estimates
CLARITY_THRESHOLD = (
    4.0  # minimum clarity (peak/noise ratio) to consider a valid whistle
)

LOCKOUT_TIME = (
    0.3  # seconds to lock out after a detected chirp to prevent multiple triggers
)

PLOT_HISTORY = 150  # number of points to show (~3 seconds)

freq_history = deque(maxlen=WINDOW_SIZE)
time_history = deque(maxlen=WINDOW_SIZE)
recent_freqs = deque(maxlen=MEDIAN_FILTER_SIZE)

plot_freqs = deque(maxlen=PLOT_HISTORY)
plot_slopes = deque(maxlen=PLOT_HISTORY)
plot_times = deque(maxlen=PLOT_HISTORY)

smooth_freq = None  # smoothed frequency estimate
last_trigger_time = 0.0  # timestamp of last detected chirp

keyboard = Controller()  # pynput keyboard controller for simulating key presses


# -----------------------------
# FFT-based dominant frequency
# -----------------------------
def dominant_frequency_and_clarity(data):
    """Compute dominant frequency and spectral clarity using FFT."""
    window = np.hanning(len(data))
    spectrum = np.fft.rfft(window * data)
    mag = np.abs(spectrum)

    peak = np.argmax(mag)
    peak_val = mag[peak]
    noise_floor = np.median(mag)

    clarity = peak_val / (noise_floor + 1e-6)
    freq = peak * RATE / len(data)

    return freq, clarity


# -----------------------------
# PyQtGraph setup
# -----------------------------
app = pg.mkQApp("Whistle Visualizer")

win = pg.GraphicsLayoutWidget(title="Whistle Frequency + Slope")
win.resize(900, 600)

# Frequency plot
p_freq = win.addPlot(title="Frequency (Hz)")
p_freq.setYRange(0, 3000)
curve_freq = p_freq.plot(pen=pg.mkPen("w", width=2))

# Slope plot
win.nextRow()
p_slope = win.addPlot(title="Slope (Hz/s)")
p_slope.setYRange(-2000, 2000)
curve_slope = p_slope.plot(pen=pg.mkPen("y", width=2))

win.show()


# -----------------------------
# Audio callback
# -----------------------------
def audio_callback(indata, frames, t, status):
    """
    Process incoming audio frames: estimate frequency, detect chirps, update plots, and simulate key presses.

    Arguments:
    - indata: numpy array of shape (frames, channels) containing audio samples
    - frames: number of samples in this block
    - t: timestamp of this block
    - status: callback status
    """
    global smooth_freq, last_trigger_time

    data = indata[:, 0]
    rms = np.sqrt(np.mean(data**2))

    # Ignore quiet frames
    if rms < AMP_THRESHOLD:
        return

    # Estimate dominant frequency and clarity
    freq, clarity = dominant_frequency_and_clarity(data)
    if clarity < CLARITY_THRESHOLD:
        return
    if not (WHISTLE_MIN <= freq <= WHISTLE_MAX):
        return

    # Median filter to stabilize frequency estimates
    recent_freqs.append(freq)
    freq = np.median(recent_freqs)

    # Exponential smoothing
    if smooth_freq is None:
        smooth_freq = freq
    else:
        smooth_freq = SMOOTH_ALPHA * freq + (1 - SMOOTH_ALPHA) * smooth_freq

    now = time.time()

    # Update history for slope estimation
    freq_history.append(smooth_freq)
    time_history.append(now)

    # Need enough samples for slope estimation
    if len(freq_history) < WINDOW_SIZE:
        return

    # Estimate slope (Hz/s) using linear regression
    t0 = np.array(time_history)
    f0 = np.array(freq_history)
    slope, _ = np.polyfit(t0 - t0[0], f0, 1)

    # Store for plotting
    plot_times.append(now)
    plot_freqs.append(smooth_freq)
    plot_slopes.append(slope)

    # Update plots
    curve_freq.setData(list(plot_freqs))
    curve_slope.setData(list(plot_slopes))

    # Lockout
    if now - last_trigger_time < LOCKOUT_TIME:
        return

    # Chirp detection
    if slope > SLOPE_THRESHOLD:
        print("⬆️  UP CHIRP → Key.UP")
        keyboard.press(Key.up)
        keyboard.release(Key.up)
        last_trigger_time = now
        curve_freq.setPen(pg.mkPen("g", width=3))

    elif slope < -SLOPE_THRESHOLD:
        print("⬇️  DOWN CHIRP → Key.DOWN")
        keyboard.press(Key.down)
        keyboard.release(Key.down)
        last_trigger_time = now
        curve_freq.setPen(pg.mkPen("r", width=3))

    else:
        curve_freq.setPen(pg.mkPen("w", width=2))


# -----------------------------
# Main
# -----------------------------
def main():
    """Start the whistle detection and visualization."""
    print(
        "Whistle detector with live frequency + slope plot. Close the plot window to stop."
    )

    with sd.InputStream(
        channels=1,
        samplerate=RATE,
        blocksize=CHUNK,
        callback=audio_callback,
        latency="low",
    ):
        pg.exec()


if __name__ == "__main__":
    main()
