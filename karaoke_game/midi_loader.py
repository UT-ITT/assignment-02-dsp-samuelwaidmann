"""
Minimal MIDI/KAR loader for the karaoke game.

Extracts note events as (start_time, duration, pitch) tuples.
"""

from mido import MidiFile


def load_midi_notes(path):
    """
    Load a MIDI or KAR file and extract note events.

    Returns:
        List of tuples: (start_time_seconds, duration_seconds, midi_pitch)
    """
    midi = MidiFile(path)
    notes = []
    ongoing = {}  # pitch -> start_time

    current_time = 0.0

    for msg in midi:
        current_time += msg.time

        if msg.type == "note_on" and msg.velocity > 0:
            # Start of a note
            ongoing[msg.note] = current_time

        elif (msg.type == "note_off") or (msg.type == "note_on" and msg.velocity == 0):
            # End of a note
            pitch = msg.note
            if pitch in ongoing:
                start = ongoing[pitch]
                duration = current_time - start
                notes.append((start, duration, pitch))
                del ongoing[pitch]

    # Sort by start time
    notes.sort(key=lambda x: x[0])
    return notes


if __name__ == "__main__":
    # Quick test
    path = "karaoke_game/abba_-_dancing_queen.kar"
    for n in load_midi_notes(path):
        print(n)
