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
import os
import logging
from typing import List, Tuple, Optional, Union
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for validation
MIN_GRID_SIZE = 1
MAX_GRID_SIZE = 100  # Reasonable limit for memory and display
VALID_GRID_CHARS = {'-', '1', '2', 'X'}

class NonogramError(Exception):
    """Custom exception for nonogram-related errors."""
    pass

class ValidationError(NonogramError):
    """Exception raised for validation errors."""
    pass

class FileOperationError(NonogramError):
    """Exception raised for file operation errors."""
    pass

def validate_grid_dimensions(width: int, height: int) -> None:
    """Validate grid dimensions are within acceptable limits."""
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValidationError("Grid dimensions must be integers")
    
    if width < MIN_GRID_SIZE or height < MIN_GRID_SIZE:
        raise ValidationError(f"Grid dimensions must be at least {MIN_GRID_SIZE}x{MIN_GRID_SIZE}")
    
    if width > MAX_GRID_SIZE or height > MAX_GRID_SIZE:
        raise ValidationError(f"Grid dimensions cannot exceed {MAX_GRID_SIZE}x{MAX_GRID_SIZE}")

def validate_grid_content(grid: List[List[str]]) -> None:
    """Validate grid content for correct format and characters."""
    if not grid:
        raise ValidationError("Grid cannot be empty")
    
    if not all(isinstance(row, list) for row in grid):
        raise ValidationError("Grid must be a list of lists")
    
    # Check for consistent row lengths
    expected_width = len(grid[0])
    if expected_width == 0:
        raise ValidationError("Grid rows cannot be empty")
    
    for i, row in enumerate(grid):
        if len(row) != expected_width:
            raise ValidationError(f"Row {i} has length {len(row)}, expected {expected_width}")
        
        # Check for valid characters
        for j, cell in enumerate(row):
            if not isinstance(cell, str):
                raise ValidationError(f"Cell at ({i}, {j}) must be a string, got {type(cell)}")
            if cell not in VALID_GRID_CHARS:
                raise ValidationError(f"Invalid character '{cell}' at ({i}, {j}). Valid characters: {VALID_GRID_CHARS}")

def parse_grid(grid_str: str) -> List[List[str]]:
    """Parse the input grid string into a 2D list with validation."""
    if not isinstance(grid_str, str):
        raise ValidationError("Grid input must be a string")
    
    grid_str = grid_str.strip()
    if not grid_str:
        raise ValidationError("Grid input cannot be empty")
    
    try:
        lines = grid_str.split('\n')
        lines = [line for line in lines if line.strip()]  # Remove empty lines
        
        if not lines:
            raise ValidationError("No valid grid lines found")
        
        grid = [list(line.strip()) for line in lines]
        validate_grid_content(grid)
        
        height, width = len(grid), len(grid[0])
        validate_grid_dimensions(width, height)
        
        logger.info(f"Successfully parsed grid: {width}x{height}")
        return grid
        
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        logger.error(f"Failed to parse grid: {e}")
        raise ValidationError(f"Failed to parse grid: {e}")

def generate_shading_clues(grid: List[List[str]]) -> Tuple[List[List[int]], List[List[int]]]:
    """Generate the phase 1 shading clues for rows and columns.
    Cells marked as '1' or 'X' are part of Phase 1 solution."""
    try:
        validate_grid_content(grid)
        
        row_clues = []
        for i, row in enumerate(grid):
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
            row_clues.append(clues if clues else [])
        
        col_clues = []
        height, width = len(grid), len(grid[0])
        for col_idx in range(width):
            clues = []
            count = 0
            for row_idx in range(height):
                cell = grid[row_idx][col_idx]
                if cell in ['1', 'X']:  # Cells to be shaded in Phase 1
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            col_clues.append(clues if clues else [])
        
        logger.debug(f"Generated shading clues: {len(row_clues)} rows, {len(col_clues)} columns")
        return row_clues, col_clues
        
    except Exception as e:
        logger.error(f"Failed to generate shading clues: {e}")
        raise NonogramError(f"Failed to generate shading clues: {e}")

def generate_erasing_clues(grid: List[List[str]]) -> Tuple[List[List[int]], List[List[int]]]:
    """Generate the phase 2 erasing clues for rows and columns.
    Cells marked as '2' or 'X' are to be erased in Phase 2."""
    try:
        validate_grid_content(grid)
        
        row_clues = []
        for i, row in enumerate(grid):
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
            row_clues.append(clues if clues else [])
        
        col_clues = []
        height, width = len(grid), len(grid[0])
        for col_idx in range(width):
            clues = []
            count = 0
            for row_idx in range(height):
                cell = grid[row_idx][col_idx]
                if cell in ['2', 'X']:  # Cells to be erased in Phase 2
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            col_clues.append(clues if clues else [])
        
        logger.debug(f"Generated erasing clues: {len(row_clues)} rows, {len(col_clues)} columns")
        return row_clues, col_clues
        
    except Exception as e:
        logger.error(f"Failed to generate erasing clues: {e}")
        raise NonogramError(f"Failed to generate erasing clues: {e}")

class NonoGramVisualizer:
    def __init__(self, grid: List[List[str]], editor_mode: bool = False):
        try:
            validate_grid_content(grid)
            
            self.grid = grid
            self.height = len(grid)
            self.width = len(grid[0])
            self.editor_mode = editor_mode
            self.editor_phase = 1  # Start with Phase 1 in editor mode
            self.click_enabled = True  # Flag to control click processing
            
            # Generate clues with error handling
            self.shading_row_clues, self.shading_col_clues = generate_shading_clues(grid)
            self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(grid)
            
            # Calculate max number of clues for sizing with safe handling
            self.max_row_clues = max((len(clues) for clues in self.shading_row_clues), default=0)
            self.max_col_clues = max((len(clues) for clues in self.shading_col_clues), default=0)
            
            # Set up the visualization
            self.fig = None
            self.ax = None
            self.current_phase = 0  # 0: empty, 1: after shading, 2: after erasing
            self.phases = ["Initial Grid", "Phase 01: Apply foundation protocol", "Phase 02: Execute refinement protocol"]
            
            if editor_mode:
                self.current_phase = 2  # Show the final state in editor mode
                
            logger.info(f"Initialized visualizer: {self.width}x{self.height}, editor_mode={editor_mode}")
            
        except Exception as e:
            logger.error(f"Failed to initialize visualizer: {e}")
            raise NonogramError(f"Failed to initialize visualizer: {e}")
        
    def setup_figure(self) -> None:
        """Set up the matplotlib figure with error handling."""
        try:
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
                
            logger.debug("Figure setup completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup figure: {e}")
            raise NonogramError(f"Failed to setup matplotlib figure: {e}")
        
    def validate_grid_coordinates(self, row: int, col: int) -> bool:
        """Validate that grid coordinates are within bounds."""
        return (0 <= row < self.height and 0 <= col < self.width)
        
    def on_click(self, event) -> None:
        """Handle mouse clicks in editor mode with validation."""
        try:
            if event.xdata is None or event.ydata is None:
                logger.debug("Click outside plot area, ignoring")
                return
            
            # Convert click coordinates to grid indices
            col = int(event.xdata)
            row = self.height - 1 - int(event.ydata)
            
            # Validate coordinates
            if not self.validate_grid_coordinates(row, col):
                logger.debug(f"Click at invalid coordinates ({row}, {col}), ignoring")
                return
                
            logger.debug(f"Processing click at grid position ({row}, {col})")
            
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
                    
            # Update clues with error handling
            try:
                self.shading_row_clues, self.shading_col_clues = generate_shading_clues(self.grid)
                self.erasing_row_clues, self.erasing_col_clues = generate_erasing_clues(self.grid)
                
                # Redraw the puzzle
                self.draw_puzzle()
                
            except Exception as clue_error:
                logger.error(f"Failed to update clues after click: {clue_error}")
                # Restore previous state if possible
                # For now, just continue with existing clues
                
        except Exception as e:
            logger.error(f"Error handling click event: {e}")
            # Don't raise exception to avoid crashing the GUI
    
    def safe_save_grid(self, filename: str) -> bool:
        """Safely save the grid to a file with comprehensive error handling."""
        try:
            # Validate filename
            if not filename or not isinstance(filename, str):
                raise ValidationError("Filename must be a non-empty string")
            
            # Check if directory exists and is writable
            directory = os.path.dirname(filename) or '.'
            if not os.path.exists(directory):
                raise FileOperationError(f"Directory does not exist: {directory}")
            
            if not os.access(directory, os.W_OK):
                raise FileOperationError(f"No write permission for directory: {directory}")
            
            # Check available disk space (basic check)
            try:
                import shutil
                free_space = shutil.disk_usage(directory).free
                if free_space < 1024:  # Less than 1KB free
                    raise FileOperationError("Insufficient disk space")
            except Exception as disk_error:
                logger.warning(f"Could not check disk space: {disk_error}")
            
            # Validate grid before saving
            validate_grid_content(self.grid)
            
            # Create backup if file exists
            backup_filename = None
            if os.path.exists(filename):
                backup_filename = filename + '.backup'
                try:
                    import shutil
                    shutil.copy2(filename, backup_filename)
                    logger.info(f"Created backup: {backup_filename}")
                except Exception as backup_error:
                    logger.warning(f"Could not create backup: {backup_error}")
            
            # Write the file
            with open(filename, 'w', encoding='utf-8') as f:
                for row in self.grid:
                    f.write(''.join(row) + '\n')
            
            # Verify the file was written correctly
            if not os.path.exists(filename):
                raise FileOperationError("File was not created successfully")
            
            # Clean up backup if write was successful
            if backup_filename and os.path.exists(backup_filename):
                try:
                    os.remove(backup_filename)
                    logger.debug("Removed backup file after successful save")
                except Exception as cleanup_error:
                    logger.warning(f"Could not remove backup file: {cleanup_error}")
            
            logger.info(f"Successfully saved grid to {filename}")
            return True
            
        except (ValidationError, FileOperationError) as e:
            logger.error(f"Save operation failed: {e}")
            raise
        except PermissionError as e:
            error_msg = f"Permission denied when saving to {filename}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except OSError as e:
            error_msg = f"OS error when saving to {filename}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error when saving to {filename}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
            
    def save_grid(self, event=None) -> None:
        """Save the current grid to a file or advance to next editor phase."""
        try:
            if self.editor_phase == 1:
                # Store grid state before transition to prevent bugs
                grid_copy = [row[:] for row in self.grid]
                
                # When in phase 1, advance to phase 2
                self.editor_phase = 2
                self.fig.suptitle("Nonogram Editor Mode - Phase 2: Erasing", fontsize=16)
                print("Phase 1 completed. Now enter the cells to erase in Phase 2.")
                
                # Update the button text if it exists
                if hasattr(self, 'save_button'):
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
                try:
                    self.safe_save_grid(filename)
                    print(f"Puzzle saved to {filename}")
                    
                    # Close the figure
                    if self.fig:
                        plt.close(self.fig)
                        
                except (ValidationError, FileOperationError) as e:
                    error_msg = f"Failed to save puzzle: {e}"
                    print(error_msg)
                    logger.error(error_msg)
                    # Don't close the figure on save failure
                    
        except Exception as e:
            error_msg = f"Error in save operation: {e}"
            logger.error(error_msg)
            print(error_msg)
            
    def next_phase(self, event=None) -> None:
        """Advance to the next visualization phase."""
        try:
            self.current_phase = (self.current_phase + 1) % 3
            self.draw_puzzle()
            logger.debug(f"Advanced to phase {self.current_phase}")
        except Exception as e:
            logger.error(f"Error advancing phase: {e}")
        
    def draw_puzzle(self) -> None:
        """Draw the puzzle with comprehensive error handling."""
        try:
            if not self.ax:
                raise NonogramError("Axes not initialized")
                
            self.ax.clear()

            # Set title based on editor phase or viewing phase
            if self.editor_mode:
                if self.editor_phase == 1:
                    self.fig.suptitle("Nonogram Editor Mode - Phase 1: Shading", fontsize=16)
                else:
                    self.fig.suptitle("Nonogram Editor Mode - Phase 2: Erasing", fontsize=16)
            else:
                phase_index = min(self.current_phase, len(self.phases) - 1)
                self.fig.suptitle(self.phases[phase_index], fontsize=16)

            # Calculate grid offsets for clues
            row_offset = max(2.5, self.max_row_clues * 0.7)
            col_offset = max(2.5, self.max_col_clues * 0.6)

            # Draw the grid with darker lines for better definition
            for i in range(self.height + 1):
                self.ax.axhline(y=i, color='#333333', linestyle='-', linewidth=1.2)
            for j in range(self.width + 1):
                self.ax.axvline(x=j, color='#333333', linestyle='-', linewidth=1.2)

            # Fill cells based on phase or editor mode with bounds checking
            for i in range(self.height):
                for j in range(self.width):
                    if not self.validate_grid_coordinates(i, j):
                        logger.warning(f"Invalid grid coordinates: ({i}, {j})")
                        continue
                        
                    cell = self.grid[i][j]

                    # Add light gray background for all cells
                    rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                           facecolor='#f0f0f0', edgecolor='#333333',
                                           alpha=1.0)
                    self.ax.add_patch(rect)

                    if self.current_phase == 0 and not self.editor_mode:  
                        # Empty grid in initial phase - just light gray background
                        pass
                    elif self.current_phase == 1 and not self.editor_mode:  
                        # Phase 1: Apply foundation protocol
                        if cell in ['1', 'X']:
                            if cell == 'X':
                                # Both phases - purple with crosshatch
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor='#8A2BE2', edgecolor='#333333',
                                                       hatch='xxx', alpha=0.9)
                            else:
                                # Phase 1 only - deep blue with lighter blue hatching
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor='#1E3A8A', edgecolor='#333333',
                                                       hatch='...', alpha=0.9)
                            self.ax.add_patch(rect)
                    else:  
                        # Phase 2 or editor mode
                        if self.editor_mode:
                            # Show different visualizations based on editor phase
                            if self.editor_phase == 1:
                                # Phase 1 editing: show only phase 1 cells
                                if cell in ['1', 'X']:
                                    if cell == 'X':
                                        # Both phases - purple with crosshatch
                                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                               facecolor='#8A2BE2', edgecolor='#333333',
                                                               hatch='xxx', alpha=0.9)
                                    else:
                                        # Phase 1 only - deep blue with lighter blue hatching
                                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                               facecolor='#1E3A8A', edgecolor='#333333',
                                                               hatch='...', alpha=0.9)
                                    self.ax.add_patch(rect)
                            else:
                                # Phase 2 editing: show all cells
                                # First show phase 1 cells
                                if cell in ['1', 'X']:
                                    if cell == 'X':
                                        # Both phases - purple with crosshatch
                                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                               facecolor='#8A2BE2', edgecolor='#333333',
                                                               hatch='xxx', alpha=0.9)
                                    else:
                                        # Phase 1 only - deep blue with lighter blue hatching
                                        rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                               facecolor='#1E3A8A', edgecolor='#333333',
                                                               hatch='...', alpha=0.9)
                                    self.ax.add_patch(rect)
                                
                                # Then highlight phase 2 cells
                                if cell in ['2']:
                                    # Phase 2 only - coral/salmon with red hatching
                                    rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                           facecolor='#FA8072', edgecolor='#333333',
                                                           hatch='///', alpha=0.9)
                                    self.ax.add_patch(rect)
                        else:
                            # Phase 2: Fill everything, then show erased cells
                            # First fill everything with phase 1 style
                            if cell in ['1', 'X']:
                                if cell == 'X':
                                    # Both phases - purple with crosshatch
                                    rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                           facecolor='#8A2BE2', edgecolor='#333333',
                                                           hatch='xxx', alpha=0.9)
                                else:
                                    # Phase 1 only - deep blue with lighter blue hatching
                                    rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                           facecolor='#1E3A8A', edgecolor='#333333',
                                                           hatch='...', alpha=0.9)
                                self.ax.add_patch(rect)
                            else:
                                # Fill remaining cells with deep blue for phase 2 context
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor='#1E3A8A', edgecolor='#333333',
                                                       hatch='...', alpha=0.9)
                                self.ax.add_patch(rect)
                            
                            # Then show cells that should be erased with coral/salmon pattern
                            if cell in ['2', 'X']:
                                rect = patches.Rectangle((j, self.height-i-1), 1, 1,
                                                       facecolor='#FA8072', edgecolor='#333333', 
                                                       hatch='///', alpha=0.9)
                                self.ax.add_patch(rect)

            # Draw clues with bounds checking
            self._draw_clues()

            # Set the view limits
            self.ax.set_xlim(-row_offset, self.width)
            self.ax.set_ylim(-1, self.height + col_offset)

            # Hide axis ticks
            self.ax.set_xticks([])
            self.ax.set_yticks([])

            plt.draw()
            logger.debug("Puzzle drawn successfully")
            
        except Exception as e:
            logger.error(f"Error drawing puzzle: {e}")
            # Try to show a basic error message on the plot
            try:
                if self.ax:
                    self.ax.text(0.5, 0.5, f"Error: {e}", transform=self.ax.transAxes,
                               ha='center', va='center', fontsize=12, color='red')
                    plt.draw()
            except:
                pass  # If even error display fails, just continue
    
    def _draw_clues(self) -> None:
        """Draw row and column clues with error handling."""
        try:
            # Row Clues
            for i in range(min(len(self.shading_row_clues), self.height)):
                clues = self.shading_row_clues[i]
                # Phase 1 clues (dark blue)
                if clues:  # Only display if there are clues
                    clue_text = ' '.join(map(str, clues))
                    self.ax.text(-0.5, self.height-i-0.5, clue_text,
                                 ha='right', va='center', fontsize=10, color='#1E3A8A', fontweight='bold')
                
                # Phase 2 clues (red)
                if i < len(self.erasing_row_clues):
                    erasing_clues = self.erasing_row_clues[i]
                    if erasing_clues:  # Only display if there are clues
                        erasing_text = ' '.join(map(str, erasing_clues))
                        self.ax.text(-0.5, self.height-i-0.8, erasing_text,
                                     ha='right', va='center', fontsize=10, color='red', fontweight='bold')

            # Column Clues
            for j in range(min(len(self.shading_col_clues), self.width)):
                clues = self.shading_col_clues[j]
                # Phase 1 clues (dark blue)
                if clues:  # Only display if there are clues
                    clue_text = '\n'.join(map(str, clues))
                    self.ax.text(j+0.5, self.height+0.1, clue_text,
                                 ha='center', va='bottom', fontsize=10, color='#1E3A8A', fontweight='bold')
                
                # Phase 2 clues (red)
                if j < len(self.erasing_col_clues):
                    erasing_clues = self.erasing_col_clues[j]
                    if erasing_clues:  # Only display if there are clues
                        erasing_text = '\n'.join(map(str, erasing_clues))
                        self.ax.text(j+0.8, self.height+0.1, erasing_text,
                                     ha='center', va='bottom', fontsize=10, color='red', fontweight='bold')
        except Exception as e:
            logger.error(f"Error drawing clues: {e}")

    def visualize(self) -> None:
        """Set up and display the nonogram visualization with error handling."""
        try:
            self.setup_figure()
            self.draw_puzzle()

            instruction = "Press ENTER to cycle modes"
            self.ax.text(self.width/2, -2.0, instruction, ha="center", va="center", 
                        fontsize=12, fontweight="bold", color="blue",
                        bbox=dict(boxstyle="round", fc="white", ec="blue", alpha=0.8))
                
            plt.tight_layout()
            plt.subplots_adjust(top=0.9, bottom=0.1)
            
            logger.info("Starting visualization display")
            plt.show()
            
        except Exception as e:
            logger.error(f"Failed to start visualization: {e}")
            print(f"Error starting visualization: {e}")
            raise NonogramError(f"Visualization failed: {e}")

    def handle_key_press(self, event) -> None:
        """Handle keyboard input for navigation and saving with error handling."""
        try:
            if not event or not hasattr(event, 'key'):
                logger.debug("Invalid key event received")
                return
                
            logger.debug(f"Key pressed: {event.key}")
            
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
                        try:
                            self.safe_save_grid(filename)
                            print(f"Puzzle saved to {filename}")
                            
                            # Close the figure
                            if self.fig:
                                plt.close(self.fig)
                                
                        except (ValidationError, FileOperationError) as e:
                            error_msg = f"Failed to save puzzle: {e}"
                            print(error_msg)
                            logger.error(error_msg)
                            # Don't close the figure on save failure
                else:
                    # In viewing mode, use Enter to advance phase
                    self.current_phase = (self.current_phase + 1) % 3
                    self.draw_puzzle()
                    
        except Exception as e:
            logger.error(f"Error handling key press: {e}")
            # Don't raise exception to avoid crashing the GUI

def safe_read_grid_file(filename: str) -> str:
    """Safely read grid data from a file with comprehensive error handling."""
    try:
        if not filename or not isinstance(filename, str):
            raise ValidationError("Filename must be a non-empty string")
        
        if not os.path.exists(filename):
            raise FileOperationError(f"File not found: {filename}")
        
        if not os.path.isfile(filename):
            raise FileOperationError(f"Path is not a file: {filename}")
        
        if not os.access(filename, os.R_OK):
            raise FileOperationError(f"No read permission for file: {filename}")
        
        # Check file size (basic safety check)
        file_size = os.path.getsize(filename)
        if file_size == 0:
            raise ValidationError(f"File is empty: {filename}")
        
        max_file_size = 1024 * 1024  # 1MB limit
        if file_size > max_file_size:
            raise ValidationError(f"File too large (>{max_file_size} bytes): {filename}")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            raise ValidationError(f"File contains no valid content: {filename}")
        
        logger.info(f"Successfully read file: {filename} ({file_size} bytes)")
        return content
        
    except (ValidationError, FileOperationError) as e:
        logger.error(f"File read failed: {e}")
        raise
    except PermissionError as e:
        error_msg = f"Permission denied when reading {filename}: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)
    except UnicodeDecodeError as e:
        error_msg = f"File encoding error in {filename}: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)
    except OSError as e:
        error_msg = f"OS error when reading {filename}: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error when reading {filename}: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg)

def process_nonogram(grid_str: str) -> None:
    """Process the nonogram grid and visualize it with error handling."""
    try:
        grid = parse_grid(grid_str)
        visualizer = NonoGramVisualizer(grid)
        visualizer.visualize()
        
    except (ValidationError, NonogramError) as e:
        error_msg = f"Failed to process nonogram: {e}"
        logger.error(error_msg)
        print(f"Error: {error_msg}")
        sys.exit(1)
    except Exception as e:
        error_msg = f"Unexpected error processing nonogram: {e}"
        logger.error(error_msg)
        print(f"Unexpected error: {error_msg}")
        sys.exit(1)

def create_empty_grid(width: int, height: int) -> List[List[str]]:
    """Create an empty grid with specified dimensions and validation."""
    try:
        validate_grid_dimensions(width, height)
        grid = [['-' for _ in range(width)] for _ in range(height)]
        logger.info(f"Created empty grid: {width}x{height}")
        return grid
        
    except ValidationError as e:
        logger.error(f"Failed to create grid: {e}")
        raise

def get_user_input_dimensions() -> Tuple[int, int]:
    """Get grid dimensions from user with validation and error handling."""
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            width_input = input("Enter puzzle width: ").strip()
            height_input = input("Enter puzzle height: ").strip()
            
            if not width_input or not height_input:
                raise ValidationError("Dimensions cannot be empty")
            
            try:
                width = int(width_input)
                height = int(height_input)
            except ValueError as e:
                raise ValidationError(f"Dimensions must be integers: {e}")
            
            validate_grid_dimensions(width, height)
            logger.info(f"User provided dimensions: {width}x{height}")
            return width, height
            
        except ValidationError as e:
            attempts_left = max_attempts - attempt - 1
            print(f"Error: {e}")
            if attempts_left > 0:
                print(f"Please try again. {attempts_left} attempts remaining.")
            else:
                raise ValidationError("Maximum attempts exceeded for dimension input")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except EOFError:
            print("\nEnd of input reached.")
            sys.exit(0)

def main() -> None:
    """Main function with comprehensive error handling."""
    try:
        print("Squared Away Nonogram Generator")
        logger.info("Starting nonogram application")

        # Check if input is from a file/pipe or keyboard
        if not sys.stdin.isatty():
            # Reading from file or pipe
            try:
                grid_str = sys.stdin.read()
                if not grid_str.strip():
                    raise ValidationError("No input data provided")
                
                logger.info("Processing input from stdin")
                process_nonogram(grid_str)
                
            except ValidationError as e:
                print(f"Input validation error: {e}")
                logger.error(f"Input validation failed: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Error reading from stdin: {e}")
                logger.error(f"Stdin read error: {e}")
                sys.exit(1)
        else:
            # Editor mode - interactive input
            try:
                print("Editor Mode: Create a new nonogram puzzle")
                print(f"Valid grid dimensions: {MIN_GRID_SIZE}-{MAX_GRID_SIZE}")
                print(f"Valid characters: {', '.join(sorted(VALID_GRID_CHARS))}")
                
                width, height = get_user_input_dimensions()
                grid = create_empty_grid(width, height)
                
                logger.info("Starting editor mode")
                visualizer = NonoGramVisualizer(grid, editor_mode=True)
                visualizer.visualize()
                
            except ValidationError as e:
                print(f"Validation error: {e}")
                logger.error(f"Editor mode validation failed: {e}")
                sys.exit(1)
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                logger.info("Application cancelled by user")
                sys.exit(0)
            except Exception as e:
                print(f"Unexpected error in editor mode: {e}")
                logger.error(f"Editor mode unexpected error: {e}")
                sys.exit(1)
                
    except Exception as e:
        print(f"Critical error in main: {e}")
        logger.critical(f"Critical error in main function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()