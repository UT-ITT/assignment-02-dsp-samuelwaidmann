[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/yaOQIQlj)

# Tasks

## 1. Karaoke Game

A lightweight karaoke game where you sing into your microphone and try to match the pitch of scrolling notes. The game visualizes your pitch in real time, scores your accuracy, and shows a final summary at the end of the song.

### Installation

1. Install Python.
2. Install dependencies:
```pip install -r requirements.txt```
3. Place your MIDI file in karaoke_game/ (default: sing_along.mid).

### Running the Game

Start the game with
```python karaoke.py```
from the home directory of the repository.

Make sure your microphone is connected and recognized by the system.

### Sources Used for Inspiration
- https://dnmtechs.com/real-time-sound-processing-in-python-3-capturing-and-analyzing-microphone-input/
- https://www.c-sharpcorner.com/article/compute-fft-for-audio-pitch-detection-real-time-vocal-coach-for-singers-using-p/
- https://github.com/Akshayalakshmi-P/Real-Time-Pitch-Tracker-and-Note-detection

### Additional Features One Could Add
- pitch deviation meter
- vibrato smoothing
- a progress bar for the song
- suppress the terminal warnings when starting the game


## 2. Whistle Input

Recommended Packages: matplotlib, numpy, pyaudio, pynput
Create a program called whistle-input.py that detects whistled frequency chirps and reacts to them
in real time. Frequency chirps are signals that change their frequency over time, for example,
“ooouuuiii” for an upwards chirp and “iiiuuuooo” for a downwards chirp. Use the pynput library to
trigger key presses (up and down arrow) to navigate in arbitrary GUI menus by whistling.
Score
(3P) upwards and downwards whistling is detected correctly and robustly
(2P) detection is robust against background noise
(1P) low latency between input and detection
(1P) triggered key events work

(1P) Well-structured and readable code, virtual environment is used
