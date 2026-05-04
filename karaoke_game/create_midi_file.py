"""This script creates a simple MIDI file with a sequence of notes for the karaoke game."""

from midiutil import MIDIFile

# 1. Setup the MIDI object
# One track, defaults to time 0
track = 0
time = 0
midi_file = MIDIFile(1)
midi_file.addTrackName(track, time, "Sing Along Track")
midi_file.addTempo(track, time, 100)  # Moderate, singable tempo

# 2. Define the notes (C Major Scale)
# MIDI pitch 60 is Middle C
# 15 notes: C-D-E-F-G-A-B-C (up) then B-A-G-F-E-D-C (down)
pitch_sequence = [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60]

channel = 0
volume = 100  # 0-127
duration = 1  # 1 beat per note

# 3. Add notes to the track
for i, pitch in enumerate(pitch_sequence):
    midi_file.addNote(track, channel, pitch, time + i, duration, volume)

# 4. Save the file
filename = "karaoke_game/sing_along.mid"
with open(filename, "wb") as output_file:
    midi_file.writeFile(output_file)

print(f"Success! Created {filename} with 15 notes.")
