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
        import random
        import math
        
        # Multiple themed color palettes for maximum fun!
        color_themes = {
            'pastel_dream': [
                '#f7f7f7', '#ffe0f7', '#e0f7fa', '#fffde7', '#e1bee7', '#f8bbd0',
                '#dcedc8', '#ffe082', '#b2dfdb', '#c5cae9', '#f0f4c3', '#ffecb3',
                '#b3e5fc', '#d1c4e9', '#c8e6c9', '#ffccbc', '#f5f5f5', '#e6ee9c',
                '#fce4ec', '#f3e5f5', '#e0f2f1', '#f9fbe7', '#fff9c4', '#fbe9e7'
            ],
            'tropical_paradise': [
                '#ffeb3b', '#ff9800', '#ff5722', '#e91e63', '#9c27b0', '#673ab7',
                '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50',
                '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722'
            ],
            'galaxy_cosmic': [
                '#1a237e', '#3949ab', '#5e35b1', '#7b1fa2', '#ad1457', '#c62828',
                '#d84315', '#e65100', '#ef6c00', '#f57c00', '#ff8f00', '#ff6f00',
                '#e040fb', '#d500f9', '#aa00ff', '#7c4dff', '#536dfe', '#448aff'
            ],
            'ocean_depths': [
                '#006064', '#00838f', '#0097a7', '#00acc1', '#00bcd4', '#26c6da',
                '#4dd0e1', '#80deea', '#b2ebf2', '#e0f7fa', '#84ffff', '#18ffff',
                '#00e5ff', '#00b8d4', '#0091ea', '#2979ff', '#304ffe', '#3d5afe'
            ],
            'sunset_vibes': [
                '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315',
                '#bf360c', '#ff9800', '#ff8f00', '#ff6f00', '#e65100', '#d84315',
                '#ffcc02', '#ffb300', '#ff8f00', '#ff6f00', '#ff5722', '#e64a19'
            ],
            'rainbow_explosion': [
                '#ff0000', '#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00',
                '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffbf',
                '#00ffff', '#00bfff', '#0080ff', '#0040ff', '#0000ff', '#4000ff',
                '#8000ff', '#bf00ff', '#ff00ff', '#ff00bf', '#ff0080', '#ff0040'
            ]
        }
        
        # Select a random theme for this visualization
        current_theme = random.choice(list(color_themes.keys()))
        pastel_palette = color_themes[current_theme]
        
        # Dynamic phase colors that change based on position for gradient effects
        def get_gradient_color(base_color, i, j, max_i, max_j):
            """Generate gradient color based on position"""
            # Create a slight color variation based on position
            pos_factor = (i + j) / (max_i + max_j) if (max_i + max_j) > 0 else 0
            
            # Convert hex to RGB
            base_color = base_color.lstrip('#')
            r, g, b = tuple(int(base_color[k:k+2], 16) for k in (0, 2, 4))
            
            # Apply position-based variation
            r = min(255, max(0, int(r + (pos_factor * 50 - 25))))
            g = min(255, max(0, int(g + (pos_factor * 50 - 25))))
            b = min(255, max(0, int(b + (pos_factor * 50 - 25))))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        
        # Holographic color schemes with shimmer effects
        holographic_phase1 = ['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#fb5607']
        holographic_phase2 = ['#f72585', '#b5179e', '#7209b7', '#480ca8', '#3f37c9', '#4361ee']
        holographic_both = ['#ff9500', '#ff8500', '#ff7700', '#ff6600', '#ff5500', '#ff4400']
        
        color_phase1 = random.choice(holographic_phase1)
        color_phase2 = random.choice(holographic_phase2) 
        color_both = random.choice(holographic_both)
        
        # Vibrant grid and accent colors
        neon_accents = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00', '#ff4081', '#64ffda']
        color_grid = random.choice(neon_accents)
        color_erase = random.choice(['#ff1744', '#e91e63', '#ad1457', '#880e4f'])
        color_phase1_alt = get_gradient_color(color_phase1, 1, 1, self.height, self.width)
        color_phase2_alt = get_gradient_color(color_phase2, 1, 1, self.height, self.width)
        color_both_alt = get_gradient_color(color_both, 1, 1, self.height, self.width)
        color_x_highlight = random.choice(['#ff80ab', '#ff4081', '#f50057', '#c51162'])

        for i in range(self.height):
            for j in range(self.width):
                cell = self.grid[i][j]
                # Create dynamic color selection based on position for shimmer effect
                color_empty = pastel_palette[(i + j * 3) % len(pastel_palette)]
                
                # Add sparkle effect with random alpha variations
                sparkle_alpha = 0.85 + random.random() * 0.15
                
                if self.current_phase == 0 and not self.editor_mode:
                    # Empty grid in initial phase with gradient shimmer
                    gradient_empty = get_gradient_color(color_empty, i, j, self.height, self.width)
                    rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                           facecolor=gradient_empty, edgecolor=color_grid, 
                                           alpha=sparkle_alpha, linewidth=2)
                    self.ax.add_patch(rect)
                elif self.current_phase == 1 and not self.editor_mode:
                    # Phase 1: Apply foundation protocol with holographic effects
                    if cell == '1':
                        phase1_gradient = get_gradient_color(color_phase1, i, j, self.height, self.width)
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor=phase1_gradient, edgecolor=color_grid, 
                                               alpha=sparkle_alpha, linewidth=2)
                        self.ax.add_patch(rect)
                    elif cell == 'X':
                        both_gradient = get_gradient_color(color_both, i, j, self.height, self.width)
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor=both_gradient, edgecolor=color_x_highlight, 
                                               alpha=sparkle_alpha, hatch='xx', linewidth=2)
                        self.ax.add_patch(rect)
                    else:
                        # Empty cells still get fun colors
                        gradient_empty = get_gradient_color(color_empty, i, j, self.height, self.width)
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor=gradient_empty, edgecolor=color_grid, 
                                               alpha=sparkle_alpha * 0.7, linewidth=1)
                        self.ax.add_patch(rect)
                else:
                    # Phase 2 or editor mode with enhanced visual effects
                    if self.editor_mode:
                        # Show different visualizations based on editor phase
                        if self.editor_phase == 1:
                            # Phase 1 editing: show only phase 1 cells with vibrant colors
                            if cell == '1':
                                phase1_alt_gradient = get_gradient_color(color_phase1_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=phase1_alt_gradient, edgecolor=color_grid, 
                                                       alpha=sparkle_alpha, linewidth=2)
                                self.ax.add_patch(rect)
                            elif cell == 'X':
                                both_alt_gradient = get_gradient_color(color_both_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=both_alt_gradient, edgecolor=color_x_highlight, 
                                                       alpha=sparkle_alpha, hatch='xx', linewidth=2)
                                self.ax.add_patch(rect)
                            else:
                                # Empty cells get themed background
                                gradient_empty = get_gradient_color(color_empty, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=gradient_empty, edgecolor=color_grid, 
                                                       alpha=sparkle_alpha * 0.6, linewidth=1)
                                self.ax.add_patch(rect)
                        else:
                            # Phase 2 editing: show all cells with maximum color vibrancy
                            # First show phase 1 cells
                            if cell == '1':
                                phase1_alt_gradient = get_gradient_color(color_phase1_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=phase1_alt_gradient, edgecolor=color_grid, 
                                                       alpha=sparkle_alpha, linewidth=2)
                                self.ax.add_patch(rect)
                            elif cell == 'X':
                                both_alt_gradient = get_gradient_color(color_both_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=both_alt_gradient, edgecolor=color_x_highlight, 
                                                       alpha=sparkle_alpha, hatch='xx', linewidth=2)
                                self.ax.add_patch(rect)
                            # Then highlight phase 2 cells with spectacular effects
                            if cell == '2':
                                phase2_alt_gradient = get_gradient_color(color_phase2_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=phase2_alt_gradient, edgecolor=color_grid, 
                                                       alpha=sparkle_alpha, hatch='///', linewidth=2)
                                self.ax.add_patch(rect)
                            elif cell == 'X':
                                # Double-layer effect for X cells
                                both_alt_gradient = get_gradient_color(color_both_alt, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=both_alt_gradient, edgecolor=color_x_highlight, 
                                                       alpha=sparkle_alpha, hatch='///', linewidth=3)
                                self.ax.add_patch(rect)
                            if cell == '-':
                                # Empty cells get subtle themed background
                                gradient_empty = get_gradient_color(color_empty, i, j, self.height, self.width)
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor=gradient_empty, edgecolor=color_grid, 
                                                       alpha=sparkle_alpha * 0.5, linewidth=1)
                                self.ax.add_patch(rect)
                    else:
                        # Phase 2: Fill everything, then show erased cells with rainbow effects
                        phase1_gradient = get_gradient_color(color_phase1, i, j, self.height, self.width)
                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                               facecolor=phase1_gradient, edgecolor=color_grid, 
                                               alpha=sparkle_alpha, linewidth=2)
                        self.ax.add_patch(rect)
                        # Then show cells that should be erased with a distinctive pattern
                        if cell == '2':
                            phase2_gradient = get_gradient_color(color_phase2, i, j, self.height, self.width)
                            rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                   facecolor=phase2_gradient, edgecolor=color_erase, 
                                                   alpha=sparkle_alpha, hatch='///', linewidth=3)
                            self.ax.add_patch(rect)
                        elif cell == 'X':
                            both_gradient = get_gradient_color(color_both, i, j, self.height, self.width)
                            rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                   facecolor=both_gradient, edgecolor=color_x_highlight, 
                                                   alpha=sparkle_alpha, hatch='///', linewidth=3)
                            self.ax.add_patch(rect)


        # -- Row Clues --
        # Super vibrant color collections for maximum visual impact
        cosmic_colors = ['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#fb5607', '#ff4081', '#e040fb']
        neon_colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00', '#ff1744', '#2979ff', '#ff9100', '#00e676']
        rainbow_gradient = ['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080']
        
        for i, clues in enumerate(self.shading_row_clues):
            # -- Phase 1 clues (cosmic rainbow with position-based color) --
            clue_text = ' '.join(map(str, clues))
            clue_color = cosmic_colors[i % len(cosmic_colors)]
            # Add gradient effect to text color
            text_alpha = 0.9 + (i % 3) * 0.03  # Slight alpha variation
            self.ax.text(-0.5, self.height-i-0.5, clue_text,
                         ha='right', va='center', fontsize=11, color=clue_color, 
                         fontweight='bold', alpha=text_alpha,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7, edgecolor=clue_color))
            
            # -- Phase 2 clues (neon explosion) --
            erasing_clues = self.erasing_row_clues[i]
            if erasing_clues != [0]:
                erasing_text = ' '.join(map(str, erasing_clues))
                erase_color = neon_colors[i % len(neon_colors)]
                self.ax.text(-0.5, self.height-i-0.8, erasing_text,
                             ha='right', va='center', fontsize=11, color=erase_color, 
                             fontweight='bold', alpha=text_alpha,
                             bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8, edgecolor=erase_color))

        # -- Column Clues --
        for j, clues in enumerate(self.shading_col_clues):
            # -- Phase 1 clues (rainbow gradient with shimmer) --
            clue_text = '\n'.join(map(str, clues))
            clue_color = rainbow_gradient[j % len(rainbow_gradient)]
            text_alpha = 0.9 + (j % 3) * 0.03
            self.ax.text(j+0.5, self.height+0.1, clue_text,
                         ha='center', va='bottom', fontsize=11, color=clue_color, 
                         fontweight='bold', alpha=text_alpha,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7, edgecolor=clue_color))
            
            # -- Phase 2 clues (holographic effect) --
            erasing_clues = self.erasing_col_clues[j]
            if erasing_clues != [0]:
                erasing_text = '\n'.join(map(str, erasing_clues))
                # Create holographic color shift effect
                holo_colors = ['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#fb5607']
                erase_color = holo_colors[(j + self.current_phase) % len(holo_colors)]
                self.ax.text(j+0.8, self.height+0.1, erasing_text,
                             ha='center', va='bottom', fontsize=11, color=erase_color, 
                             fontweight='bold', alpha=text_alpha,
                             bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8, edgecolor=erase_color))

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

        # Fun colorful instruction with theme announcement
        instruction_colors = ['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#fb5607']
        instruction_color = random.choice(instruction_colors)
        instruction = "Press ENTER to cycle modes"
        
        # Also show current theme
        # Access current_theme from draw_puzzle scope - we'll print it instead
        theme_instruction = f"🎨 Colorful Nonogram Visualization! 🌈"
        
        self.ax.text(self.width/2, -2.0, instruction, ha="center", va="center", 
                    fontsize=12, fontweight="bold", color=instruction_color,
                    bbox=dict(boxstyle="round", fc="white", ec=instruction_color, alpha=0.9))
        
        self.ax.text(self.width/2, -2.8, theme_instruction, ha="center", va="center", 
                    fontsize=10, fontweight="bold", color=instruction_color,
                    bbox=dict(boxstyle="round", fc=instruction_color, ec="white", alpha=0.2))
            
        plt.tight_layout()
        plt.subplots_adjust(top=0.9, bottom=0.15)
        print("🎨 Welcome to the Enhanced Colorful Nonogram Experience! 🌈")
        print("Each visualization uses a randomly selected vibrant theme!")
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

def main():
    print("Squared Away Nonogram Generator")

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
            if width <= 0 or height <= 0:
                print("Dimensions must be positive integers")
                return
                
            grid = create_empty_grid(width, height)
            visualizer = NonoGramVisualizer(grid, editor_mode=True)
            visualizer.visualize()
            
        except ValueError:
            print("Please enter valid integers for dimensions")

if __name__ == "__main__":
    main()