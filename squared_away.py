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
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def parse_grid(grid_str):
    """Parse the input grid string into a 3D list.
    For 2D compatibility, single layer grids are supported.
    3D grids should have layers separated by blank lines."""
    lines = [line.strip() for line in grid_str.strip().split('\n') if line.strip()]
    
    # Check if this is a 3D grid (contains blank line separators in original)
    original_lines = grid_str.strip().split('\n')
    has_blank_lines = any(line.strip() == '' for line in original_lines)
    
    if has_blank_lines:
        # 3D format: layers separated by blank lines
        layers = []
        current_layer = []
        
        for line in original_lines:
            line = line.strip()
            if line == '':
                if current_layer:
                    layers.append([list(row) for row in current_layer])
                    current_layer = []
            else:
                current_layer.append(line)
        
        # Add the last layer
        if current_layer:
            layers.append([list(row) for row in current_layer])
        
        return layers
    else:
        # 2D format: convert to single layer 3D format for compatibility
        return [[list(line) for line in lines]]

def generate_shading_clues(grid):
    """Generate the phase 1 shading clues for all three axes.
    Cells marked as '1' or 'X' are part of Phase 1 solution."""
    depth = len(grid)
    height = len(grid[0])
    width = len(grid[0][0])
    
    # Row clues (x-axis, for each y,z coordinate)
    row_clues = []
    for z in range(depth):
        layer_clues = []
        for y in range(height):
            clues = []
            count = 0
            for x in range(width):
                cell = grid[z][y][x]
                if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            layer_clues.append(clues if clues else [0])
        row_clues.append(layer_clues)
    
    # Column clues (y-axis, for each x,z coordinate)
    col_clues = []
    for z in range(depth):
        layer_clues = []
        for x in range(width):
            clues = []
            count = 0
            for y in range(height):
                cell = grid[z][y][x]
                if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            layer_clues.append(clues if clues else [0])
        col_clues.append(layer_clues)
    
    # Depth clues (z-axis, for each x,y coordinate)
    depth_clues = []
    for y in range(height):
        row_clues_layer = []
        for x in range(width):
            clues = []
            count = 0
            for z in range(depth):
                cell = grid[z][y][x]
                if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            row_clues_layer.append(clues if clues else [0])
        depth_clues.append(row_clues_layer)
    
    return row_clues, col_clues, depth_clues

def generate_erasing_clues(grid):
    """Generate the phase 2 erasing clues for all three axes.
    Cells marked as '2' or 'X' are to be erased in Phase 2."""
    depth = len(grid)
    height = len(grid[0])
    width = len(grid[0][0])
    
    # Row clues (x-axis, for each y,z coordinate)
    row_clues = []
    for z in range(depth):
        layer_clues = []
        for y in range(height):
            clues = []
            count = 0
            for x in range(width):
                cell = grid[z][y][x]
                if cell in ['2', 'X']:  # Cells to be erased in Phase 2
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            layer_clues.append(clues if clues else [0])
        row_clues.append(layer_clues)
    
    # Column clues (y-axis, for each x,z coordinate)
    col_clues = []
    for z in range(depth):
        layer_clues = []
        for x in range(width):
            clues = []
            count = 0
            for y in range(height):
                cell = grid[z][y][x]
                if cell in ['2', 'X']:  # Cells to be erased in Phase 2
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            layer_clues.append(clues if clues else [0])
        col_clues.append(layer_clues)
    
    # Depth clues (z-axis, for each x,y coordinate)
    depth_clues = []
    for y in range(height):
        row_clues_layer = []
        for x in range(width):
            clues = []
            count = 0
            for z in range(depth):
                cell = grid[z][y][x]
                if cell in ['2', 'X']:  # Cells to be erased in Phase 2
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            row_clues_layer.append(clues if clues else [0])
        depth_clues.append(row_clues_layer)
    
    return row_clues, col_clues, depth_clues

class NonoGramVisualizer:
    def __init__(self, grid, editor_mode=False):
        self.grid = grid
        self.depth = len(grid)
        self.height = len(grid[0])
        self.width = len(grid[0][0])
        self.editor_mode = editor_mode
        self.editor_phase = 1  # Start with Phase 1 in editor mode
        self.click_enabled = True  # Flag to control click processing
        self.current_layer = 0  # Current layer being viewed/edited
        
        # Generate clues
        self.shading_row_clues, self.shading_col_clues, self.shading_depth_clues = generate_shading_clues(grid)
        self.erasing_row_clues, self.erasing_col_clues, self.erasing_depth_clues = generate_erasing_clues(grid)
        
        # Calculate max number of clues for sizing
        max_row_clues = 0
        max_col_clues = 0
        for layer in self.shading_row_clues:
            for clues in layer:
                max_row_clues = max(max_row_clues, len(clues))
        for layer in self.shading_col_clues:
            for clues in layer:
                max_col_clues = max(max_col_clues, len(clues))
        
        self.max_row_clues = max_row_clues
        self.max_col_clues = max_col_clues
        
        # Set up the visualization
        self.fig = None
        self.ax = None
        self.current_phase = 0  # 0: empty, 1: after shading, 2: after erasing
        self.phases = ["Initial Grid", "Phase 01: Apply foundation protocol", "Phase 02: Execute refinement protocol"]
        
        if editor_mode:
            self.current_phase = 2  # Show the final state in editor mode
        
    def setup_figure(self):
        # Create the figure with 3D projection
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set title based on current phase
        if self.editor_mode:
            self.fig.suptitle(f"Nonogram Editor Mode - Phase 1: Shading (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
        else:
            self.fig.suptitle(f"{self.phases[self.current_phase]} (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
        
        # Create keyboard binding for navigation
        if not self.editor_mode:
            self.fig.canvas.mpl_connect('key_press_event', self.handle_key_press)
        else:
            # Connect the click event for editor mode
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            # Connect keyboard event for editor mode
            self.fig.canvas.mpl_connect('key_press_event', self.handle_key_press)
        
    def draw_cube(self, x, y, z, facecolor='gray', edgecolor='black', alpha=0.7):
        """Draw a 3D cube at the given coordinates"""
        # Define the vertices of a cube
        vertices = [
            [x, y, z], [x+1, y, z], [x+1, y+1, z], [x, y+1, z],  # bottom face
            [x, y, z+1], [x+1, y, z+1], [x+1, y+1, z+1], [x, y+1, z+1]  # top face
        ]
        
        # Define the 6 faces of the cube
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # front face
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # right face
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # back face
            [vertices[3], vertices[0], vertices[4], vertices[7]],  # left face
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # top face
            [vertices[0], vertices[3], vertices[2], vertices[1]]   # bottom face
        ]
        
        # Create a Poly3DCollection and add it to the axes
        try:
            cube = Poly3DCollection(faces, facecolors=facecolor, edgecolors=edgecolor, alpha=alpha)
            self.ax.add_collection3d(cube)
            return cube
        except Exception as e:
            print(f"Error creating cube at ({x},{y},{z}): {e}")
            return None

    def on_click(self, event):
        """Handle mouse clicks in editor mode"""
        if event.xdata is None or event.ydata is None:
            return
        
        # Convert click coordinates to grid indices (simplified for current layer)
        x = int(event.xdata)
        y = int(event.ydata)
        z = self.current_layer
        
        # Check if the click is within the current layer grid
        if 0 <= y < self.height and 0 <= x < self.width and 0 <= z < self.depth:
            # Handle clicks based on the current editor phase
            if self.editor_phase == 1:
                # Phase 1: Toggle between empty (-) and phase 1 (1)
                if self.grid[z][y][x] == '-':
                    self.grid[z][y][x] = '1'
                else:
                    self.grid[z][y][x] = '-'
            else:  # editor_phase == 2
                # Phase 2: Toggle between empty (-) and phase 2 (2)
                if self.grid[z][y][x] == '-':
                    self.grid[z][y][x] = '2'
                elif self.grid[z][y][x] == '1':
                    self.grid[z][y][x] = 'X'  # Both phase 1 and 2
                elif self.grid[z][y][x] == 'X':
                    self.grid[z][y][x] = '1'  # Back to just phase 1
                elif self.grid[z][y][x] == '2':
                    self.grid[z][y][x] = '-'  # Back to empty
                
            # Update clues
            self.shading_row_clues, self.shading_col_clues, self.shading_depth_clues = generate_shading_clues(self.grid)
            self.erasing_row_clues, self.erasing_col_clues, self.erasing_depth_clues = generate_erasing_clues(self.grid)
            
            # Redraw the puzzle
            self.draw_puzzle()
    
    def save_grid(self, event=None):
        """Save the current grid to a file or advance to next editor phase"""
        if self.editor_phase == 1:
            # Store grid state before transition to prevent bugs
            grid_copy = [[[cell for cell in row] for row in layer] for layer in self.grid]
            
            # When in phase 1, advance to phase 2
            self.editor_phase = 2
            self.fig.suptitle(f"Nonogram Editor Mode - Phase 2: Erasing (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
            print("Phase 1 completed. Now enter the cells to erase in Phase 2.")
            
            # Update the button text if it exists
            if hasattr(self, 'save_button'):
                self.save_button.label.set_text("Complete")
            
            # Restore grid state to prevent unwanted changes
            self.grid = grid_copy
            
            # Update clues and redraw
            self.shading_row_clues, self.shading_col_clues, self.shading_depth_clues = generate_shading_clues(self.grid)
            self.erasing_row_clues, self.erasing_col_clues, self.erasing_depth_clues = generate_erasing_clues(self.grid)
            self.draw_puzzle()
        else:
            # When in phase 2, save the completed puzzle
            filename = "nonogram_puzzle_3d.txt"
            with open(filename, 'w') as f:
                for z, layer in enumerate(self.grid):
                    if z > 0:
                        f.write('\n')  # Blank line between layers
                    for row in layer:
                        f.write(''.join(row) + '\n')
            print(f"3D Puzzle saved to {filename}")
            
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
                self.fig.suptitle(f"Nonogram Editor Mode - Phase 1: Shading (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
            else:
                self.fig.suptitle(f"Nonogram Editor Mode - Phase 2: Erasing (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
        else:
            self.fig.suptitle(f"{self.phases[self.current_phase]} (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)

        # Draw cubes based on phase or editor mode
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.grid[z][y][x]
                    
                    # Show all layers with transparency when not in editor mode
                    # In editor mode, focus on current layer
                    alpha = 0.7 if z == self.current_layer or not self.editor_mode else 0.2

                    if self.current_phase == 0 and not self.editor_mode:  
                        # Empty grid in initial phase - show wireframe only for current layer
                        if z == self.current_layer:
                            self.draw_cube(x, y, z, facecolor='white', edgecolor='black', alpha=0.1)
                    elif self.current_phase == 1 and not self.editor_mode:  
                        # Phase 1: Apply foundation protocol
                        if cell in ['1', 'X']:
                            self.draw_cube(x, y, z, facecolor='gray', edgecolor='black', alpha=alpha)
                        elif z == self.current_layer:
                            self.draw_cube(x, y, z, facecolor='white', edgecolor='lightgray', alpha=0.1)
                    else:  
                        # Phase 2 or editor mode
                        if self.editor_mode:
                            # Show different visualizations based on editor phase
                            if self.editor_phase == 1:
                                # Phase 1 editing: show only phase 1 cells
                                if cell in ['1', 'X']:
                                    self.draw_cube(x, y, z, facecolor='gray', edgecolor='black', alpha=alpha)
                                elif z == self.current_layer:
                                    self.draw_cube(x, y, z, facecolor='white', edgecolor='lightgray', alpha=0.1)
                            else:
                                # Phase 2 editing: show all cells
                                # Show wireframe for current layer
                                if z == self.current_layer:
                                    self.draw_cube(x, y, z, facecolor='white', edgecolor='lightgray', alpha=0.1)
                                
                                # First show phase 1 cells
                                if cell in ['1', 'X']:
                                    self.draw_cube(x, y, z, facecolor='gray', edgecolor='black', alpha=alpha)
                                
                                # Then highlight phase 2 cells
                                if cell in ['2', 'X']:
                                    self.draw_cube(x, y, z, facecolor='red', edgecolor='darkred', alpha=alpha)
                        else:
                            # Phase 2: Fill everything, then show erased cells
                            # First fill everything
                            self.draw_cube(x, y, z, facecolor='gray', edgecolor='black', alpha=alpha)
                            
                            # Then show cells that should be erased with a distinctive pattern
                            if cell in ['2', 'X']:
                                self.draw_cube(x, y, z, facecolor='red', edgecolor='darkred', alpha=alpha)

        # Set the view limits
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_zlim(0, self.depth)

        # Label the axes
        self.ax.set_xlabel('X (Width)')
        self.ax.set_ylabel('Y (Height)')
        self.ax.set_zlabel('Z (Depth)')

        # Set view angle for better visibility
        self.ax.view_init(elev=20, azim=45)

        plt.draw()

    def visualize(self):
        self.setup_figure()
        self.draw_puzzle()

        if self.editor_mode:
            instruction = "Press ENTER to advance phase, UP/DOWN to change layers"
        else:
            instruction = "Press ENTER to cycle phases, UP/DOWN to change layers"
        
        # Add instruction text outside the 3D plot
        self.fig.text(0.5, 0.02, instruction, ha="center", va="center", 
                     fontsize=12, fontweight="bold", color="blue",
                     bbox=dict(boxstyle="round", fc="white", ec="blue", alpha=0.8))
            
        plt.tight_layout()
        plt.show()

    def handle_key_press(self, event):
        """Handle keyboard input for navigation and saving"""
        if event.key == 'enter':
            if self.editor_mode:
                # In editor mode, use Enter to advance phase or save
                if self.editor_phase == 1:
                    # Store grid state before transition to prevent bugs
                    grid_copy = [[[cell for cell in row] for row in layer] for layer in self.grid]
                    
                    # Advance to phase 2
                    self.editor_phase = 2
                    self.fig.suptitle(f"Nonogram Editor Mode - Phase 2: Erasing (Layer {self.current_layer + 1}/{self.depth})", fontsize=16)
                    print("Phase 1 completed. Now enter the cells to erase in Phase 2.")
                    
                    # Restore grid state to prevent unwanted changes
                    self.grid = grid_copy
                    
                    # Update clues and redraw
                    self.shading_row_clues, self.shading_col_clues, self.shading_depth_clues = generate_shading_clues(self.grid)
                    self.erasing_row_clues, self.erasing_col_clues, self.erasing_depth_clues = generate_erasing_clues(self.grid)
                    self.draw_puzzle()
                else:
                    # Save the completed puzzle
                    filename = "nonogram_puzzle_3d.txt"
                    with open(filename, 'w') as f:
                        for z, layer in enumerate(self.grid):
                            if z > 0:
                                f.write('\n')  # Blank line between layers
                            for row in layer:
                                f.write(''.join(row) + '\n')
                    print(f"3D Puzzle saved to {filename}")
                    
                    # Close the figure
                    plt.close(self.fig)
            else:
                # In viewing mode, use Enter to advance phase
                self.current_phase = (self.current_phase + 1) % 3
                self.draw_puzzle()
        elif event.key == 'up':
            # Move to next layer
            self.current_layer = min(self.current_layer + 1, self.depth - 1)
            self.draw_puzzle()
        elif event.key == 'down':
            # Move to previous layer
            self.current_layer = max(self.current_layer - 1, 0)
            self.draw_puzzle()

def process_nonogram(grid_str):
    """Process the nonogram grid and visualize it."""
    grid = parse_grid(grid_str)
    visualizer = NonoGramVisualizer(grid)
    visualizer.visualize()

def create_empty_grid(width, height, depth=1):
    """Create an empty grid with specified dimensions."""
    return [[['-' for _ in range(width)] for _ in range(height)] for _ in range(depth)]

def main():
    print("Squared Away 3D Nonogram Generator")

    # Check if input is from a file/pipe or keyboard
    if not sys.stdin.isatty():
        # Reading from file or pipe
        grid_str = sys.stdin.read()
        process_nonogram(grid_str)
    else:
        # Editor mode
        try:
            width = int(input("Enter puzzle width: "))
            height = int(input("Enter puzzle height: "))
            depth = int(input("Enter puzzle depth (layers): "))
            if width <= 0 or height <= 0 or depth <= 0:
                print("Dimensions must be positive integers")
                return
                
            grid = create_empty_grid(width, height, depth)
            visualizer = NonoGramVisualizer(grid, editor_mode=True)
            visualizer.visualize()
            
        except ValueError:
            print("Please enter valid integers for dimensions")

if __name__ == "__main__":
    main()