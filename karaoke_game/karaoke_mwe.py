"""This module implements a simple pitch detection algorithm using FFT to convert microphone input into musical notes in real-time."""

import pyaudio
import numpy as np
import math

# -----------------------------
# Configuration
# -----------------------------
CHUNK = 1024  # Number of audio samples per frame
RATE = 22050  # Sampling rate (Hz)
VOCAL_MIN = 80  # Hz
VOCAL_MAX = 1000  # Hz
AMP_THRESHOLD = 500  # Silence threshold
SMOOTHING = 3  # Moving average window size

# Precompute Hann window
# The Hann window helps reduce spectral leakage in the FFT, improving pitch detection accuracy.
# see https://en.wikipedia.org/wiki/Hann_function
HANN = np.hanning(CHUNK)

# For smoothing
last_freqs = []


# -----------------------------
# Frequency → MIDI → Note
# -----------------------------
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def freq_to_midi(f):
    """Convert frequency in Hz to MIDI note number."""
    return 69 + 12 * math.log2(f / 440.0)


def midi_to_note(m):
    """Convert MIDI note number to note name (e.g., 60 → C4)."""
    m = int(round(m))
    name = NOTE_NAMES[m % 12]
    octave = m // 12 - 1
    return f"{name}{octave}"


# -----------------------------
# Pitch Detection (FFT)
# -----------------------------
def detect_pitch(data):
    """
    Detect the fundamental frequency from raw audio data using FFT.

    Arguments:
        data: bytes of audio data from the microphone (16-bit PCM).
    Returns:
        freq: Detected frequency in Hz, or None if no valid pitch is detected.
    """
    # Convert bytes to numpy array
    audio = np.frombuffer(data, dtype=np.int16)

    # Amplitude check (silence)
    if np.abs(audio).mean() < AMP_THRESHOLD:
        return None

    # Apply Hann window
    windowed = audio * HANN

    # FFT
    spectrum = np.fft.rfft(windowed)
    magnitudes = np.abs(spectrum)

    # Ignore DC
    magnitudes[0] = 0

    # Peak frequency
    peak_index = np.argmax(magnitudes)
    freq = peak_index * RATE / CHUNK

    # Vocal range filter
    if freq < VOCAL_MIN or freq > VOCAL_MAX:
        return None

    return freq


# -----------------------------
# Main Loop
# -----------------------------
def main():
    """Capture audio and detect pitch in real-time."""
    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Listening... (Ctrl+C to stop)")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            freq = detect_pitch(data)

            if freq is None:
                print("—", end="\r")
                continue

            # Smoothing
            last_freqs.append(freq)
            if len(last_freqs) > SMOOTHING:
                last_freqs.pop(0)
            freq_smoothed = sum(last_freqs) / len(last_freqs)

            # Convert to note
            midi = freq_to_midi(freq_smoothed)
            note = midi_to_note(midi)

            print(f"{freq_smoothed:7.1f} Hz  →  {note}", end="\r")

    except KeyboardInterrupt:
        print("\nStopping...")

    stream.stop_stream()
    stream.close()
    pa.terminate()


if __name__ == "__main__":
    main()
