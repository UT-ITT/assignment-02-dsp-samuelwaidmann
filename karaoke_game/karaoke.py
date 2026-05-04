"""Main module for the karaoke game. It sets up the audio processing, timeline, scoring, and visualization."""

import threading
import pyaudio
import time
from karaoke_mwe import detect_pitch, freq_to_midi, CHUNK, RATE
from midi_loader import load_midi_notes
from timeline import SongTimeline
from scoring import ScoringSystem
from visualizer import KaraokeVisualizer
from end_detector import SongEndDetector
from smoother import PitchSmoother


def audio_thread(timeline, scoring, vis, end_detector, smoother):
    """Thread function to capture audio, detect pitch, and update scoring and visualization."""
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    timeline.start()

    while True:
        # Check for restart request
        if vis.request_restart:
            vis.request_restart = False
            scoring.reset()
            timeline.start()
            vis.restart()
            continue

        # Do nothing during start or pause
        if vis.mode in ("start", "pause", "countdown"):
            time.sleep(0.01)
            continue

        # Read audio and detect pitch
        data = stream.read(CHUNK, exception_on_overflow=False)
        freq = detect_pitch(data)

        # Update time
        t = timeline.get_current_time()
        vis.current_time = t

        # Check for end of song
        if end_detector.is_finished(t):
            vis.accuracy = scoring.accuracy()
            vis.show_summary()
            continue

        # Get expected note
        expected = timeline.get_current_note()
        if expected is None:
            vis.expected_midi = None
            vis.sung_midi = None
            continue

        expected_pitch, start, end = expected
        vis.expected_midi = expected_pitch

        # If no pitch detected, update scoring with None and continue
        if freq is None:
            scoring.update(expected_pitch, None)
            vis.sung_midi = None
            vis.score = scoring.score
            continue

        # Convert detected frequency to MIDI note and update scoring
        sung_midi_raw = freq_to_midi(freq)
        sung_midi_smooth = smoother.update(sung_midi_raw)  # APPLY SMOOTHING
        is_correct = scoring.update(expected_pitch, sung_midi_smooth)
        vis.sung_midi = sung_midi_smooth
        vis.score = scoring.score

        # Add player bar for visualization
        if sung_midi_smooth is not None:
            vis.add_player_bar(sung_midi_smooth, t, is_correct)


def main():
    """Main function to set up the karaoke game."""
    notes = load_midi_notes("karaoke_game/sing_along.mid")
    timeline = SongTimeline(notes)
    scoring = ScoringSystem()
    end_detector = SongEndDetector(notes)
    smoother = PitchSmoother(alpha=0.2)  # ← ADD THIS

    vis = KaraokeVisualizer(notes, timeline, scoring)

    t = threading.Thread(
        target=audio_thread,
        args=(timeline, scoring, vis, end_detector, smoother),  # ← PASS IT
        daemon=True,
    )
    t.start()

    vis.run()


if __name__ == "__main__":
    main()
