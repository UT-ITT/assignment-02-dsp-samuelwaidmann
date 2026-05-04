"""
This module implements the visualizer for the karaoke game using pyglet.
It displays the note bars, player performance, score, and handles the start/pause/summary screens.
"""

import pyglet
from pyglet import shapes
from pyglet.window import key

PIXELS_PER_SECOND = 100


class NoteBar:
    """Represents a single note bar in the visualization, which scrolls horizontally as the song plays."""

    def __init__(self, start, duration, midi, visualizer):
        """Initialize a single note bar in the visualization."""
        self.start = start
        self.end = start + duration
        self.midi = midi
        self.vis = visualizer

        # Initial position (will be updated every frame)
        y = self.vis.midi_to_y(midi)
        width = duration * PIXELS_PER_SECOND

        self.rect = shapes.Rectangle(
            x=0,
            y=y,
            width=width,
            height=6,
            color=(255, 255, 255),
            batch=self.vis.bg_batch,
        )

    def update(self, current_time):
        """Update the position of the note bar based on the current time."""
        # Horizontal scrolling: notes move left as time increases
        x = 400 + (self.start - current_time) * PIXELS_PER_SECOND
        self.rect.x = x

        # Update vertical position in case pitch mapping changes
        self.rect.y = self.vis.midi_to_y(self.midi)


class PlayerBar:
    """Represents a short-lived bar that appears when the player sings a note, showing the detected pitch and whether it was correct."""

    def __init__(self, midi, time, vis, correct):
        """Initialize a player performance bar that appears when the player sings a note."""
        self.midi = midi
        self.time = time
        self.vis = vis
        self.correct = correct
        self.age = 0.0

        y = vis.midi_to_y(midi)

        # Paul Tol colors
        GREEN = (68, 187, 153)
        RED = (238, 136, 102)

        color = GREEN if correct else RED

        self.rect = shapes.Rectangle(
            x=400, y=y, width=6, height=8, color=color, batch=vis.bg_batch
        )

    def update(self, current_time, dt):
        """Update the position and appearance of the player bar, and return False if it should be removed."""
        # Move left with the timeline
        x = 400 + (self.time - current_time) * PIXELS_PER_SECOND
        self.rect.x = x

        # Update vertical position
        self.rect.y = self.vis.midi_to_y(self.midi)

        # Age for fade-out
        self.age += dt

        # Fade alpha over 1 second
        fade = max(0, 1 - self.age / 1.0)
        self.rect.opacity = int(255 * fade)

        return fade > 0


class KaraokeVisualizer:
    """Main visualizer class for the karaoke game, handling all rendering and UI elements."""

    def __init__(self, notes, timeline, scoring):
        """Initialize the karaoke visualizer with the song notes, timeline, and scoring system."""
        self.window = pyglet.window.Window(800, 400, "Karaoke")

        # Shared state
        self.expected_midi = None
        self.sung_midi = None
        self.score = 0
        self.accuracy = 0.0
        self.current_time = 0.0
        self.mode = "play"
        self.request_restart = False
        self.timeline = timeline
        self.scoring = scoring

        ui_color = (153, 221, 255, 255)  # 99DDFF

        self.bg_batch = pyglet.graphics.Batch()  # note bars, player bars
        self.ui_batch = pyglet.graphics.Batch()  # dim overlay + labels

        self.dim_overlay = shapes.Rectangle(
            x=0, y=0, width=800, height=400, color=(0, 0, 0), batch=self.ui_batch
        )
        self.dim_overlay.opacity = 0  # hidden by default

        self.countdown_label = pyglet.text.Label(
            "",
            x=400,
            y=200,
            anchor_x="center",
            anchor_y="center",
            font_size=48,
            color=ui_color,
            batch=self.bg_batch,
        )

        # Note bars
        self.note_bars = [
            NoteBar(start, dur, midi, self) for (start, dur, midi) in notes
        ]

        self.player_bars = []

        self.mode = "start"  # default mode

        self.start_label = pyglet.text.Label(
            "KARAOKE GAME\n\nPress SPACE to start.\nPress SPACE again to pause or resume.\nPress R to restart.",
            x=400,
            y=250,
            anchor_x="center",
            anchor_y="center",
            font_size=24,
            multiline=True,
            width=600,
            color=ui_color,
            batch=self.ui_batch,
        )

        self.pause_label = pyglet.text.Label(
            "PAUSED\n\nPress SPACE to resume.\nPress R to restart.",
            x=400,
            y=250,
            anchor_x="center",
            anchor_y="center",
            font_size=24,
            multiline=True,
            width=600,
            color=ui_color,
            batch=self.ui_batch,
        )

        # Hide pause label initially
        self.pause_label.text = ""

        # Score label
        self.score_label = pyglet.text.Label(
            "Score: 0 of 0",
            x=10,
            y=370,
            font_size=16,
            color=ui_color,
            batch=self.ui_batch,
        )

        # Summary label
        self.summary_label = pyglet.text.Label(
            "",
            x=400,
            y=200,
            anchor_x="center",
            anchor_y="center",
            font_size=24,
            color=ui_color,
            multiline=True,
            width=600,
            batch=self.ui_batch,
        )

        @self.window.event
        def on_draw():
            """Render the current frame, including note bars, player bars, and UI elements."""
            self.window.clear()
            self.bg_batch.draw()  # gameplay elements
            self.ui_batch.draw()  # overlays + UI

        @self.window.event
        def on_key_press(symbol, modifiers):
            """Handle key presses for starting, pausing, resuming, and restarting the game."""
            # Restart always available
            if symbol == key.R:
                self.request_restart = True
                return

            # SPACE controls start/pause/resume
            if symbol == key.SPACE:
                if self.mode == "start":
                    self.start_label.text = ""
                    self.mode = "countdown"
                    self.start_countdown(lambda: self._begin_play())

                elif self.mode == "play":
                    # go to pause
                    self.mode = "pause"
                    self.pause_label.text = (
                        "PAUSED\n\nPress SPACE to resume\nPress R to restart"
                    )
                    self.timeline.pause()

                elif self.mode == "pause":
                    # resume from pause
                    self.pause_label.text = ""
                    self.mode = "countdown"
                    self.start_countdown(lambda: self._resume_play())

        pyglet.clock.schedule_interval(self.update, 1 / 60)

    def _begin_play(self):
        """Start the game after the initial countdown."""
        self.mode = "play"
        self.timeline.resume()

    def _resume_play(self):
        """Resume the game after pausing."""
        self.mode = "play"
        self.timeline.resume()

    def midi_to_y(self, midi):
        """Convert a MIDI note number to a vertical Y position for visualization."""
        if midi is None:
            return -100
        return 50 + midi * 3

    def show_summary(self):
        """Display the summary screen with final score and accuracy after the song finishes."""

        def _apply(dt):
            self.mode = "summary"
            self.start_label.text = ""
            self.pause_label.text = ""
            self.summary_label.text = (
                f"Song Finished!\n"
                f"Final Score: {self.score} of {self.scoring.total_frames}\n"
                f"Accuracy: {self.accuracy * 100:.1f}%\n\n"
                f"Press R to restart"
            )

        pyglet.clock.schedule_once(_apply, 0)

    def add_player_bar(self, midi, time, correct):
        """Add a player performance bar to the visualization when the player sings a note."""

        def _apply(dt):
            self.player_bars.append(PlayerBar(midi, time, self, correct))

        pyglet.clock.schedule_once(_apply, 0)

    def restart(self):
        """Reset the game state and return to the start screen."""

        def _apply(dt):
            self.mode = "start"
            self.score = 0
            self.accuracy = 0.0
            self.current_time = 0.0
            self.sung_midi = None
            self.expected_midi = None
            self.summary_label.text = ""
            self.pause_label.text = ""
            self.score_label.text = "Score: 0 of 0"
            self.start_label.text = (
                "KARAOKE GAME\n\nPress SPACE to start\n"
                "Press SPACE again to pause/resume\n"
                "Press R to restart anytime"
            )
            self.timeline.start()

        pyglet.clock.schedule_once(_apply, 0)

    def start_countdown(self, callback):
        """Show 3-2-1 countdown, then call callback() to start/resume."""

        def step(n):
            if n > 0:
                self.countdown_label.text = str(n)
                pyglet.clock.schedule_once(lambda dt: step(n - 1), 1.0)
            else:
                self.countdown_label.text = "GO!"
                pyglet.clock.schedule_once(lambda dt: finish(), 0.5)

        def finish():
            self.countdown_label.text = ""
            callback()

        step(3)

    def update(self, dt):
        """Update the visualization every frame, including note bars, player bars, and UI elements based on the current game mode."""
        if self.mode in ("start", "pause", "summary"):
            self.dim_overlay.opacity = 255
            return

        self.dim_overlay.opacity = 0  # hide dim overlay during play

        # Normal gameplay
        for bar in self.note_bars:
            bar.update(self.current_time)

        alive = []
        for pbar in self.player_bars:
            if pbar.update(self.current_time, dt):
                alive.append(pbar)
        self.player_bars = alive

        self.score_label.text = f"Score: {self.score} of {self.scoring.total_frames}"

    def run(self):
        """Start the visualizer application."""
        pyglet.app.run()
