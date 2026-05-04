[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/yaOQIQlj)

# Tasks

## 1. Karaoke Game

Recommended Packages: matplotlib, numpy, pyaudio, pyglet
Create a program called karaoke.py that captures audio from your computer’s microphone and
detects the sound’s major frequency in real time. Use this frequency as input for a small audio-based
karaoke game. You can generate notes at random, specify them in a list in your code, or read a midi
file. Build your own karaoke game for a song, including an enjoyable pyglet interface. The song
should contain at least 15 notes.
Score
(3P) frequency detection works correctly and robustly
(2P) the game is playable, does not crash, and is (kind of) fun to play
(1P) the game tracks some kind of score for correctly sung notes
(1P) low latency between input and detection


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
