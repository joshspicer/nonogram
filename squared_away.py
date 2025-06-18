#!/usr/bin/env python3
"""
Squared Away Nonogram Generator

This program generates clues for a two-phase nonogram puzzle:
- Phase 1: Shading clues 
           (standard nonogram rules)
- Phase 2: Erasing clues 
           (standard nonogram rules, but the entire grid is filled to start and the clues indicate erasing)

The program also visualizes the puzzle with matplotlib and provides an editor mode.
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
    """Generate the phase 1 shading clues for rows and columns.
    Cells marked as '1' or 'X' are part of Phase 1 solution."""
    row_clues = []
    for row in grid:
        clues = []
        count = 0
        for cell in row:
            if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
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
            if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues if clues else [0])
    
    return row_clues, col_clues

def generate_erasing_clues(grid):
    """Generate the phase 2 erasing clues for rows and columns.
    Cells marked as '2' or 'X' are to be erased in Phase 2."""
    row_clues = []
    for row in grid:
        clues = []
        count = 0
        for cell in row:
            if cell in ['2', 'X']:  # Cells to be erased in Phase 2
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
            if cell in ['2', 'X']:  # Cells to be erased in Phase 2
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues if clues else [0])
    
    return row_clues, col_clues

class NonoGramVisualizer:
    def __init__(self, grid, editor_mode=False):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.editor_mode = editor_mode
        self.editor_phase = 1  # Start with Phase 1 in editor mode
        self.click_enabled = True  # Flag to control click processing
        
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
        
        if editor_mode:
            self.current_phase = 2  # Show the final state in editor mode
        
    def setup_figure(self):
        # Create the figure with enough space for clues
        self.fig, self.ax = plt.subplots()
        
        # Set title based on current phase
        if self.editor_mode:
            self.fig.suptitle("Nonogram Editor Mode - Phase 1: Shading", fontsize=16)
        else:
            self.fig.suptitle(self.phases[self.current_phase], fontsize=16)
        
        # Create keyboard binding for navigation
        if not self.editor_mode:
            self.fig.canvas.mpl_connect('key_press_event', self.handle_key_press)
        else:
            # Connect the click event for editor mode
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            # Connect keyboard event for editor mode
            self.fig.canvas.mpl_connect('key_press_event', self.handle_key_press)
        
    def on_click(self, event):
        """Handle mouse clicks in editor mode"""
        if event.xdata is None or event.ydata is None:
            return
        
        # Convert click coordinates to grid indices
        col = int(event.xdata)
        row = self.height - 1 - int(event.ydata)
        
        # Check if the click is within the grid
        if 0 <= row < self.height and 0 <= col < self.width:
            # Handle clicks based on the current editor phase
            if self.editor_phase == 1:
                # Phase 1: Toggle between empty (-) and phase 1 (1)
                if self.grid[row][col] == '-':
                    self.grid[row][col] = '1'
                else:
                    self.grid[row][col] = '-'
            else:  # editor_phase == 2
                # Phase 2: Toggle between empty (-) and phase 2 (2)
                if self.grid[row][col] == '-':
                    self.grid[row][col] = '2'
                elif self.grid[row][col] == '1':
                    self.grid[row][col] = 'X'  # Both phase 1 and 2
                elif self.grid[row][col] == 'X':
                    self.grid[row][col] = '1'  # Back to just phase 1
                elif self.grid[row][col] == '2':
                    self.grid[row][col] = '-'  # Back to empty
                
            # Update clues
            self.shading_row_clues, self.shading_col_clues = generate_shading_clues(self.grid)
            self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(self.grid)
            
            # Redraw the puzzle
            self.draw_puzzle()
    
    def save_grid(self, event=None):
        """Save the current grid to a file or advance to next editor phase"""
        if self.editor_phase == 1:
            # Store grid state before transition to prevent bugs
            grid_copy = [row[:] for row in self.grid]
            
            # When in phase 1, advance to phase 2
            self.editor_phase = 2
            self.fig.suptitle("Nonogram Editor Mode - Phase 2: Erasing", fontsize=16)
            print("Phase 1 completed. Now enter the cells to erase in Phase 2.")
            
            # Update the button text
            self.save_button.label.set_text("Complete")
            
            # Restore grid state to prevent unwanted changes
            self.grid = grid_copy
            
            # Update clues and redraw
            self.shading_row_clues, self.shading_col_clues = generate_shading_clues(self.grid)
            self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(self.grid)
            self.draw_puzzle()
        else:
            # When in phase 2, save the completed puzzle
            filename = "nonogram_puzzle.txt"
            with open(filename, 'w') as f:
                for row in self.grid:
                    f.write(''.join(row) + '\n')
            print(f"Puzzle saved to {filename}")
            
            # Close the figure
            plt.close(self.fig)
            
    def next_phase(self, event=None):
        self.current_phase = (self.current_phase + 1) % 3
        self.draw_puzzle()
        
    def draw_puzzle(self):
        self.ax.clear()

        # Set title based on editor phase or viewing phase
        if self.editor_mode:
            if self.editor_phase == 1:
                self.fig.suptitle("Nonogram Editor Mode - Phase 1: Shading", fontsize=16)
            else:
                self.fig.suptitle("Nonogram Editor Mode - Phase 2: Erasing", fontsize=16)
        else:
            self.fig.suptitle(self.phases[self.current_phase], fontsize=16)

        # Calculate grid offsets for clues
        row_offset = max(2.5, self.max_row_clues * 0.7)
        col_offset = max(2.5, self.max_col_clues * 0.6)

        # Draw the grid
        for i in range(self.height + 1):
            self.ax.axhline(y=i, color='black', linestyle='-', linewidth=1)
        for j in range(self.width + 1):
            self.ax.axvline(x=j, color='black', linestyle='-', linewidth=1)

        # Fill cells based on phase or editor mode
        for i in range(self.height):
            for j in range(self.width):
                cell = self.grid[i][j]

                if self.current_phase == 0 and not self.editor_mode:  
                    # Empty grid in initial phase
                    pass
                elif self.current_phase == 1 and not self.editor_mode:  
                    # Phase 1: Apply foundation protocol
                    if cell in ['1', 'X']:
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor='gray', edgecolor='black',
                                               hatch='xxx', alpha=0.7)
                        self.ax.add_patch(rect)
                else:  
                    # Phase 2 or editor mode
                    if self.editor_mode:
                        # Show different visualizations based on editor phase
                        if self.editor_phase == 1:
                            # Phase 1 editing: show only phase 1 cells
                            if cell in ['1', 'X']:
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                     facecolor='gray', edgecolor='black',
                                                     hatch='xxx', alpha=0.7)
                                self.ax.add_patch(rect)
                        else:
                            # Phase 2 editing: show all cells
                            # First show phase 1 cells
                            if cell in ['1', 'X']:
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                     facecolor='gray', edgecolor='black')
                                self.ax.add_patch(rect)
                            
                            # Then highlight phase 2 cells
                            if cell in ['2', 'X']:
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                     facecolor='white', edgecolor='black',
                                                     hatch='///', alpha=0.7)
                                self.ax.add_patch(rect)
                    else:
                        # Phase 2: Fill everything, then show erased cells
                        # First fill everything
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor='gray', edgecolor='black')
                        self.ax.add_patch(rect)
                        
                        # Then show cells that should be erased with a distinctive pattern
                        if cell in ['2', 'X']:
                            rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                 facecolor='white', edgecolor='black', 
                                                 hatch='///', alpha=0.7)
                            self.ax.add_patch(rect)

        # -- Row Clues --
        for i, clues in enumerate(self.shading_row_clues):
            # -- Phase 1 clues (black) --
            clue_text = ' '.join(map(str, clues))
            self.ax.text(-0.5, self.height-i-0.5, clue_text,
                         ha='right', va='center', fontsize=10)
            
            # -- Phase 2 clues (red) --
            erasing_clues = self.erasing_row_clues[i]
            if erasing_clues != [0]:
                erasing_text = ' '.join(map(str, erasing_clues))
                self.ax.text(-0.5, self.height-i-0.8, erasing_text,
                             ha='right', va='center', fontsize=10, color='red')

        # -- Column Clues --
        for j, clues in enumerate(self.shading_col_clues):
            # -- Phase 1 clues (black) --
            clue_text = '\n'.join(map(str, clues))
            self.ax.text(j+0.5, self.height+0.1, clue_text,
                         ha='center', va='bottom', fontsize=10)
            
            # -- Phase 2 clues (red) --
            erasing_clues = self.erasing_col_clues[j]
            if erasing_clues != [0]:
                erasing_text = '\n'.join(map(str, erasing_clues))
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

        instruction = "Press ENTER to cycle modes"
        self.ax.text(self.width/2, -2.0, instruction, ha="center", va="center", 
                    fontsize=12, fontweight="bold", color="blue",
                    bbox=dict(boxstyle="round", fc="white", ec="blue", alpha=0.8))
            
        plt.tight_layout()
        plt.subplots_adjust(top=0.9, bottom=0.1)
        plt.show()

    def handle_key_press(self, event):
        """Handle keyboard input for navigation and saving"""
        if event.key == 'enter':
            if self.editor_mode:
                # In editor mode, use Enter to advance phase or save
                if self.editor_phase == 1:
                    # Store grid state before transition to prevent bugs
                    grid_copy = [row[:] for row in self.grid]
                    
                    # Advance to phase 2
                    self.editor_phase = 2
                    self.fig.suptitle("Nonogram Editor Mode - Phase 2: Erasing", fontsize=16)
                    print("Phase 1 completed. Now enter the cells to erase in Phase 2.")
                    
                    # Restore grid state to prevent unwanted changes
                    self.grid = grid_copy
                    
                    # Update clues and redraw
                    self.shading_row_clues, self.shading_col_clues = generate_shading_clues(self.grid)
                    self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(self.grid)
                    self.draw_puzzle()
                else:
                    # Save the completed puzzle
                    filename = "nonogram_puzzle.txt"
                    with open(filename, 'w') as f:
                        for row in self.grid:
                            f.write(''.join(row) + '\n')
                    print(f"Puzzle saved to {filename}")
                    
                    # Close the figure
                    plt.close(self.fig)
            else:
                # In viewing mode, use Enter to advance phase
                self.current_phase = (self.current_phase + 1) % 3
                self.draw_puzzle()

def process_nonogram(grid_str):
    """Process the nonogram grid and visualize it."""
    grid = parse_grid(grid_str)
    visualizer = NonoGramVisualizer(grid)
    visualizer.visualize()

def create_empty_grid(width, height):
    """Create an empty grid with specified dimensions."""
    return [['-' for _ in range(width)] for _ in range(height)]

def select_difficulty():
    """Display difficulty selection menu and return selected difficulty"""
    print("\nSelect difficulty level:")
    print("1. Easy (5x5 simple patterns)")
    print("2. Medium (7x15 moderate patterns)")  
    print("3. Hard (15x19 complex patterns)")
    print("4. Editor Mode (create new puzzle)")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("Please enter 1, 2, 3, or 4")
        except (ValueError, EOFError):
            print("Please enter 1, 2, 3, or 4")

def list_puzzles(difficulty):
    """List available puzzles for the given difficulty"""
    import os
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    puzzle_dir = f"puzzles/{difficulty_map[difficulty]}"
    
    if not os.path.exists(puzzle_dir):
        print(f"No puzzles found for {difficulty_map[difficulty]} difficulty")
        return []
    
    puzzle_files = [f for f in os.listdir(puzzle_dir) if f.endswith('.txt')]
    if not puzzle_files:
        print(f"No puzzles found for {difficulty_map[difficulty]} difficulty")
        return []
    
    print(f"\nAvailable {difficulty_map[difficulty]} puzzles:")
    for i, puzzle in enumerate(puzzle_files, 1):
        print(f"{i}. {puzzle[:-4].replace('_', ' ').title()}")
    
    return puzzle_files

def select_puzzle(puzzle_files, difficulty):
    """Let user select a specific puzzle"""
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    
    while True:
        try:
            choice = input(f"\nSelect puzzle (1-{len(puzzle_files)}): ").strip()
            puzzle_idx = int(choice) - 1
            if 0 <= puzzle_idx < len(puzzle_files):
                puzzle_path = f"puzzles/{difficulty_map[difficulty]}/{puzzle_files[puzzle_idx]}"
                return puzzle_path
            else:
                print(f"Please enter a number between 1 and {len(puzzle_files)}")
        except (ValueError, EOFError):
            print(f"Please enter a number between 1 and {len(puzzle_files)}")

def main():
    print("Squared Away Nonogram Generator")

    # Check if input is from a file/pipe or keyboard
    if not sys.stdin.isatty():
        # Reading from file or pipe - maintain backward compatibility
        grid_str = sys.stdin.read()
        process_nonogram(grid_str)
    else:
        # Interactive mode - show difficulty selection
        difficulty = select_difficulty()
        
        if difficulty == '4':
            # Editor mode
            try:
                width = int(input("Enter puzzle width: "))
                height = int(input("Enter puzzle height: "))
                if width <= 0 or height <= 0:
                    print("Dimensions must be positive integers")
                    return
                    
                grid = create_empty_grid(width, height)
                visualizer = NonoGramVisualizer(grid, editor_mode=True)
                visualizer.visualize()
                
            except ValueError:
                print("Please enter valid integers for dimensions")
        else:
            # Puzzle selection mode
            puzzle_files = list_puzzles(difficulty)
            if puzzle_files:
                puzzle_path = select_puzzle(puzzle_files, difficulty)
                try:
                    with open(puzzle_path, 'r') as f:
                        grid_str = f.read()
                    process_nonogram(grid_str)
                except FileNotFoundError:
                    print(f"Puzzle file not found: {puzzle_path}")
                except Exception as e:
                    print(f"Error loading puzzle: {e}")

if __name__ == "__main__":
    main()