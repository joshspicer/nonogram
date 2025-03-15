#!/usr/bin/env python3
"""
Squared Away Nonogram Generator

This program generates clues for a two-phase nonogram puzzle:
- Phase 1: Shading clues (standard nonogram rules)
- Phase 2: Erasing clues (indicating that any shaded cells in that range should be erased)

The program also visualizes the puzzle with matplotlib.
"""
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import numpy as np

def parse_grid(grid_str):
    """Parse the input grid string into a 2D list."""
    return [list(line.strip()) for line in grid_str.strip().split('\n')]

def generate_shading_clues(grid):
    """Generate the phase 1 shading clues for rows and columns."""
    row_clues = []
    for row in grid:
        clues = []
        count = 0
        for cell in row:
            if cell in ['#', 'X']:  # Both # and X are initially shaded
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        row_clues.append(clues if clues else [0])
    
    col_clues = []
    for col_idx in range(len(grid[0])):
        clues = []
        count = 0
        for row_idx in range(len(grid)):
            cell = grid[row_idx][col_idx]
            if cell in ['#', 'X']:  # Both # and X are initially shaded
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues if clues else [0])
    
    return row_clues, col_clues

def generate_erasing_clues(grid):
    """Generate the phase 2 erasing clues for rows and columns."""
    row_clues = []
    for row in grid:
        clues = []
        start = None
        for i, cell in enumerate(row):
            if cell == 'X' and start is None:
                start = i + 1  # 1-based indexing
            elif cell != 'X' and start is not None:
                clues.append((start, i))  # end is exclusive in 1-based index
                start = None
        if start is not None:
            clues.append((start, len(row)))
        row_clues.append(clues)
    
    col_clues = []
    for col_idx in range(len(grid[0])):
        clues = []
        start = None
        for row_idx in range(len(grid)):
            cell = grid[row_idx][col_idx]
            if cell == 'X' and start is None:
                start = row_idx + 1  # 1-based indexing
            elif cell != 'X' and start is not None:
                clues.append((start, row_idx))  # end is exclusive in 1-based index
                start = None
        if start is not None:
            clues.append((start, len(grid)))
        col_clues.append(clues)
    
    return row_clues, col_clues

class NonoGramVisualizer:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        
        # Generate clues
        self.shading_row_clues, self.shading_col_clues = generate_shading_clues(grid)
        self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(grid)
        
        # Calculate max number of clues for sizing
        self.max_row_clues = max(len(clues) for clues in self.shading_row_clues)
        self.max_col_clues = max(len(clues) for clues in self.shading_col_clues)
        
        # Set up the visualization
        self.fig = None
        self.ax = None
        self.current_phase = 0  # 0: empty, 1: after shading, 2: after erasing
        self.phases = ["Initial Grid", "Phase 01: Apply foundation protocol", "Phase 02: Execute refinement protocol"]
        
    def setup_figure(self):
        # Create the figure with enough space for clues
        self.fig, self.ax = plt.subplots()
        
        # Set title based on current phase
        self.fig.suptitle(self.phases[self.current_phase], fontsize=16)
        
        # Create "Next" button
        self.next_button_ax = plt.axes([0.8, 0.05, 0.1, 0.04])
        self.next_button = Button(self.next_button_ax, 'Next Phase')
        self.next_button.on_clicked(self.next_phase)
        
    def next_phase(self, event=None):
        self.current_phase = (self.current_phase + 1) % 3
        self.draw_puzzle()
        
    def format_erasing_clue(self, ranges):
        if not ranges:
            return ""
        return ", ".join([f"{start}-{end}" for start, end in ranges])
            
    def draw_puzzle(self):
        self.ax.clear()
        
        # Set title
        self.fig.suptitle(self.phases[self.current_phase], fontsize=16)
        
        # Calculate grid offsets for clues
        row_offset = max(1.5, self.max_row_clues * 0.7)
        col_offset = max(1.5, self.max_col_clues * 0.6)
        
        # Draw the grid
        for i in range(self.height + 1):
            self.ax.axhline(y=i, color='black', linestyle='-', linewidth=1)
        for j in range(self.width + 1):
            self.ax.axvline(x=j, color='black', linestyle='-', linewidth=1)
            
        # Fill cells based on phase
        for i in range(self.height):
            for j in range(self.width):
                cell = self.grid[i][j]
                
                if self.current_phase == 0:  # Empty grid
                    # All cells are white
                    pass
                elif self.current_phase == 1:  # Phase 1: After shading
                    if cell in ['#', 'X']:
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1, 
                                               facecolor='gray', edgecolor='black')
                        self.ax.add_patch(rect)
                else:  # Phase 2: After erasing
                    if cell == '#':  # Keep shaded
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1, 
                                               facecolor='gray', edgecolor='black')
                        self.ax.add_patch(rect)
                    elif cell == 'X':  # Erased cells get a different color/pattern
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1, 
                                               facecolor='white', edgecolor='black', 
                                               hatch='///', alpha=0.3)
                        self.ax.add_patch(rect)
        
        # -- Row Clues --
        for i, clues in enumerate(self.shading_row_clues):
            clue_text = ' '.join(map(str, clues))
            # -- Phase 1 --
            self.ax.text(-0.5, self.height-i-0.5, clue_text, 
                        ha='right', va='center', fontsize=10)
            # -- Phase 2 --
            erasing_text = self.format_erasing_clue(self.erasing_row_clues[i])
            if erasing_text != "None":
                self.ax.text(-0.5, self.height-i-0.8, erasing_text, 
                            ha='right', va='center', fontsize=10, color='red')
        
        # -- Column Clues --
        for j, clues in enumerate(self.shading_col_clues):
            clue_text = '\n'.join(map(str, clues))
            # -- Phase 1 --
            self.ax.text(j+0.5, self.height+0.1, clue_text, 
                        ha='center', va='bottom', fontsize=10)
            # -- Phase 2 --
            erasing_text = '\n'.join(self.format_erasing_clue(self.erasing_col_clues[j]))
            if erasing_text != "None":
                self.ax.text(j+0.8, self.height+0.1, erasing_text, 
                            ha='center', va='bottom', fontsize=10, color='red')
        
        # Set the view limits
        self.ax.set_xlim(-row_offset, self.width)
        self.ax.set_ylim(-1, self.height + col_offset)
        
        # Hide axis ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])
            
        plt.draw()
        
    def visualize(self):
        self.setup_figure()
        self.draw_puzzle()
        plt.tight_layout()
        plt.subplots_adjust(top=0.9, bottom=0.1)
        plt.show()

def process_nonogram(grid_str):
    """Process the nonogram grid and visualize it."""
    grid = parse_grid(grid_str)
    visualizer = NonoGramVisualizer(grid)
    visualizer.visualize()

def main():
    print("Squared Away Nonogram Generator")
    
    # Check if input is from a file/pipe or keyboard
    if not sys.stdin.isatty():
        # Reading from file or pipe
        grid_str = sys.stdin.read()
    else:
        # Reading from keyboard
        print("Enter your grid below. Use:")
        print("  - '-' for empty cells")
        print("  - '#' for cells that remain shaded")
        print("  - 'X' for cells that are shaded then erased")
        print("End input with a blank line.")
        
        grid_lines = []
        while True:
            line = input()
            if not line:
                break
            grid_lines.append(line)
        
        grid_str = '\n'.join(grid_lines)
    
    process_nonogram(grid_str)

if __name__ == "__main__":
    main()