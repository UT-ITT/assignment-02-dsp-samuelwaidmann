[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/yaOQIQlj)

# Tasks

## 1. Karaoke Game

A lightweight karaoke game where you sing into your microphone and try to match the pitch of scrolling notes. The game visualizes your pitch in real time, scores your accuracy, and shows a final summary at the end of the song.

### Installation

1. Install Python.
2. Create and activate a virtual environment.
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```pip install -r requirements.txt```
4. Place your MIDI file in karaoke_game/ (default: sing_along.mid).

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

This program detects whistled frequency chirps in real time and converts them into UP and DOWN arrow key presses. An upward chirp (“ooouuuiii”) triggers ↑, and a downward chirp (“iiiuuuooo”) triggers ↓. It includes noise‑robust filtering, low‑latency FFT processing, chirp‑slope detection, and live visualization.

### Installation

1. Install Python.
2. Create and activate a virtual environment.
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```pip install -r requirements.txt```
4. When using Ubuntu activate X11 sessions and ensure Qt dependencies are installed:
```sudo apt install libxcb-cursor0```
When using another OS, please refer to the [pynput documentation](https://pynput.readthedocs.io/en/latest/limitations.html#).

### Starting the Program
Run the script:
```
python3 whistle_input.py
```

A window will open showing live frequency and slope data while the program listens to your microphone.

### How to Use
- Whistle an upward sweep: triggers UP arrow.
- Whistle a downward sweep: triggers DOWN arrow

#### Use this to navigate:
- menus
- lists
- browser pages
- any interface controlled by arrow keys

#### The program includes:
- amplitude gating
- frequency‑range filtering
- median smoothing
- slope‑based chirp detection
- lockout to prevent double‑triggers
