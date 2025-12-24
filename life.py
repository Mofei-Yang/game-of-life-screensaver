import time
import random
import shutil
import sys
import os
from collections import deque


class GameOfLife:
    def __init__(self, fps=15):
        self.fps = fps
        self.alive_char = "█"  # Block character
        self.dead_char = " "
        self.history_length = 10  # Check past 10 frames for loops

        # Initialize grid and history
        self.resize_and_reset()

    def resize_and_reset(self):
        """Detects terminal size and initializes a new random grid."""
        self.columns, self.rows = shutil.get_terminal_size()
        self.rows -= 1  # Prevent scrolling jitter

        # Double-ended queue to store past states for loop detection
        self.history = deque(maxlen=self.history_length)

        # Create random grid
        self.grid = [
            [random.choice([0, 1]) for _ in range(self.columns)]
            for _ in range(self.rows)
        ]

    def count_neighbors(self, x, y):
        """Counts neighbors using toroidal wrapping (edges wrap around)."""
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue

                col = (x + j) % self.columns
                row = (y + i) % self.rows
                count += self.grid[row][col]
        return count

    def update(self):
        """Calculates the next generation and returns count of living cells."""
        new_grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        active_cells = 0

        for r in range(self.rows):
            for c in range(self.columns):
                neighbors = self.count_neighbors(c, r)
                state = self.grid[r][c]

                if state == 1:
                    if neighbors == 2 or neighbors == 3:
                        new_grid[r][c] = 1
                        active_cells += 1
                else:
                    if neighbors == 3:
                        new_grid[r][c] = 1
                        active_cells += 1

        self.grid = new_grid
        return active_cells

    def draw(self):
        """Constructs the frame string and prints it at once."""
        # \033[H moves cursor to top-left (no flickering compared to 'clear')
        output = ["\033[H"]

        for r in range(self.rows):
            line = []
            for c in range(self.columns):
                if self.grid[r][c] == 1:
                    # Green text for living cells
                    line.append(f"\033[92m{self.alive_char}\033[0m")
                else:
                    line.append(self.dead_char)
            output.append("".join(line))

        sys.stdout.write("\n".join(output))
        sys.stdout.flush()

    def run(self):
        # Setup screen
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        sys.stdout.write("\033[?25l")  # Hide Cursor

        stagnation_counter = 0

        try:
            while True:
                # 1. Check for Terminal Resize
                curr_cols, curr_rows = shutil.get_terminal_size()
                if curr_cols != self.columns or (curr_rows - 1) != self.rows:
                    self.resize_and_reset()
                    if os.name == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")

                # 2. Draw Frame
                self.draw()

                # 3. Check for Loops (Oscillators/Still Lifes)
                # If the current grid configuration exists in our recent history,
                # we are in a loop.
                if self.grid in self.history:
                    stagnation_counter += 1
                else:
                    stagnation_counter = 0

                # 4. Save state to history
                # We append a copy implies the list object is stored.
                # Since update() creates a new list object, this reference is safe.
                self.history.append(self.grid)

                # 5. Evolve
                alive_count = self.update()

                # 6. Restart Logic
                # If empty, OR if we've been stuck in a loop/still-life for ~2 seconds
                if alive_count == 0 or stagnation_counter > (self.fps * 2):
                    self.resize_and_reset()
                    stagnation_counter = 0

                time.sleep(1 / self.fps)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        # Show cursor again and reset colors
        sys.stdout.write("\033[?25h\033[0m")
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        sys.exit(0)


if __name__ == "__main__":
    game = GameOfLife(fps=20)
    game.run()
