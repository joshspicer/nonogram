#!/usr/bin/env python3
"""
Nonogram AI Solver

This module provides an AI solver for nonogram puzzles, including support
for the two-phase nonogram format used in the Squared Away application.
"""

from typing import List, Tuple, Optional, Union
import copy


class NonogramSolver:
    """AI solver for nonogram puzzles with support for two-phase solving."""
    
    def __init__(self, width: int, height: int):
        """Initialize the solver with grid dimensions."""
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
    def reset_grid(self):
        """Reset the grid to all unknown cells."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def solve_line(self, clues: List[int], current_line: List[Optional[bool]]) -> List[Optional[bool]]:
        """
        Solve a single line (row or column) given the clues and current state.
        
        Args:
            clues: List of consecutive filled cell counts for this line
            current_line: Current state of the line (None=unknown, True=filled, False=empty)
            
        Returns:
            Updated line state with as many cells determined as possible
        """
        if not clues or clues == [0]:
            # No filled cells in this line
            return [False] * len(current_line)
        
        line_length = len(current_line)
        possible_arrangements = self._generate_arrangements(clues, line_length)
        
        # Filter arrangements that are compatible with current state
        compatible_arrangements = []
        for arrangement in possible_arrangements:
            is_compatible = True
            for i, (current, arranged) in enumerate(zip(current_line, arrangement)):
                if current is not None and current != arranged:
                    is_compatible = False
                    break
            if is_compatible:
                compatible_arrangements.append(arrangement)
        
        if not compatible_arrangements:
            return current_line  # No valid arrangements found
        
        # Find cells that have the same value in all compatible arrangements
        result = current_line[:]
        for i in range(line_length):
            values = [arr[i] for arr in compatible_arrangements]
            if all(v == values[0] for v in values):
                result[i] = values[0]
        
        return result
    
    def _generate_arrangements(self, clues: List[int], line_length: int) -> List[List[bool]]:
        """Generate all possible arrangements of clues in a line."""
        if not clues or clues == [0]:
            return [[False] * line_length]
        
        arrangements = []
        
        def backtrack(pos: int, clue_idx: int, current: List[bool]):
            if clue_idx >= len(clues):
                # All clues placed, fill rest with False
                result = current[:]
                while len(result) < line_length:
                    result.append(False)
                arrangements.append(result)
                return
            
            clue_size = clues[clue_idx]
            # Calculate minimum space needed for remaining clues
            remaining_clues = clues[clue_idx + 1:]
            min_space_for_remaining = sum(remaining_clues) + len(remaining_clues)  # +1 gap between each
            
            # Try all valid starting positions for current clue
            latest_start = line_length - clue_size - min_space_for_remaining
            
            for start_pos in range(pos, latest_start + 1):
                # Create new arrangement
                new_current = current[:]
                
                # Add empty cells up to start_pos
                while len(new_current) < start_pos:
                    new_current.append(False)
                
                # Add the clue (filled cells)
                for _ in range(clue_size):
                    new_current.append(True)
                
                # Add separator (empty cell) if not the last clue
                next_pos = len(new_current)
                if clue_idx < len(clues) - 1:
                    new_current.append(False)
                    next_pos += 1
                
                # Recurse for next clue
                backtrack(next_pos, clue_idx + 1, new_current)
        
        backtrack(0, 0, [])
        return arrangements
    
    def solve_nonogram(self, row_clues: List[List[int]], col_clues: List[List[int]], 
                      max_iterations: int = 100) -> Tuple[bool, List[List[bool]]]:
        """
        Solve a nonogram puzzle using constraint propagation.
        
        Args:
            row_clues: List of clues for each row
            col_clues: List of clues for each column
            max_iterations: Maximum number of solving iterations
            
        Returns:
            Tuple of (success, solved_grid) where solved_grid uses bool values
        """
        self.reset_grid()
        
        for iteration in range(max_iterations):
            changed = False
            
            # Process rows
            for r in range(self.height):
                old_row = self.grid[r][:]
                new_row = self.solve_line(row_clues[r], self.grid[r])
                if new_row != old_row:
                    self.grid[r] = new_row
                    changed = True
            
            # Process columns
            for c in range(self.width):
                old_col = [self.grid[r][c] for r in range(self.height)]
                new_col = self.solve_line(col_clues[c], old_col)
                if new_col != old_col:
                    for r in range(self.height):
                        self.grid[r][c] = new_col[r]
                    changed = True
            
            # Check if solved
            if self._is_complete():
                # Convert None values to bool for return
                solved_grid = [[cell if cell is not None else False for cell in row] for row in self.grid]
                return True, solved_grid
            
            if not changed:
                # No progress made, might need backtracking
                break
        
        # Attempt backtracking for remaining unknown cells
        if self._has_unknowns():
            return self._solve_with_backtracking(row_clues, col_clues)
        
        # Convert None values to bool for return
        solved_grid = [[cell if cell is not None else False for cell in row] for row in self.grid]
        return False, solved_grid
    
    def _is_complete(self) -> bool:
        """Check if the grid is completely solved (no None values)."""
        for row in self.grid:
            for cell in row:
                if cell is None:
                    return False
        return True
    
    def _has_unknowns(self) -> bool:
        """Check if there are unknown cells."""
        for row in self.grid:
            for cell in row:
                if cell is None:
                    return True
        return False
    
    def _solve_with_backtracking(self, row_clues: List[List[int]], col_clues: List[List[int]]) -> Tuple[bool, List[List[bool]]]:
        """Attempt to solve remaining cells using backtracking."""
        # Find first unknown cell
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] is None:
                    # Try both values
                    for value in [False, True]:
                        # Save current state
                        old_grid = copy.deepcopy(self.grid)
                        self.grid[r][c] = value
                        
                        # Check if this assignment is valid
                        if self._is_valid_assignment(r, c, row_clues, col_clues):
                            # Recursively solve
                            success, solved_grid = self._solve_with_backtracking(row_clues, col_clues)
                            if success:
                                return True, solved_grid
                        
                        # Restore state
                        self.grid = old_grid
                    
                    # Neither value worked
                    solved_grid = [[cell if cell is not None else False for cell in row] for row in self.grid]
                    return False, solved_grid
        
        # No unknown cells left, check if solution is valid
        if self._validate_solution(row_clues, col_clues):
            solved_grid = [[cell if cell is not None else False for cell in row] for row in self.grid]
            return True, solved_grid
        
        solved_grid = [[cell if cell is not None else False for cell in row] for row in self.grid]
        return False, solved_grid
    
    def _is_valid_assignment(self, row: int, col: int, row_clues: List[List[int]], col_clues: List[List[int]]) -> bool:
        """Check if the current assignment at (row, col) could lead to a valid solution."""
        # Check if row is still solvable
        current_row = self.grid[row]
        if None not in current_row:  # Row is complete
            if not self._validate_line(current_row, row_clues[row]):
                return False
        
        # Check if column is still solvable
        current_col = [self.grid[r][col] for r in range(self.height)]
        if None not in current_col:  # Column is complete
            if not self._validate_line(current_col, col_clues[col]):
                return False
        
        return True
    
    def _validate_line(self, line: List[bool], clues: List[int]) -> bool:
        """Validate that a complete line matches its clues."""
        if not clues or clues == [0]:
            return not any(line)
        
        groups = []
        current_group = 0
        
        for cell in line:
            if cell:
                current_group += 1
            else:
                if current_group > 0:
                    groups.append(current_group)
                    current_group = 0
        
        if current_group > 0:
            groups.append(current_group)
        
        return groups == clues
    
    def _validate_solution(self, row_clues: List[List[int]], col_clues: List[List[int]]) -> bool:
        """Validate that the complete grid matches all clues."""
        # Check all rows
        for r in range(self.height):
            if not self._validate_line(self.grid[r], row_clues[r]):
                return False
        
        # Check all columns
        for c in range(self.width):
            col = [self.grid[r][c] for r in range(self.height)]
            if not self._validate_line(col, col_clues[c]):
                return False
        
        return True
    
    def solve_two_phase_nonogram(self, phase1_row_clues: List[List[int]], phase1_col_clues: List[List[int]],
                               phase2_row_clues: List[List[int]], phase2_col_clues: List[List[int]]) -> Tuple[bool, List[List[str]]]:
        """
        Solve a two-phase nonogram puzzle.
        
        Args:
            phase1_row_clues: Row clues for phase 1 (shading)
            phase1_col_clues: Column clues for phase 1 (shading)
            phase2_row_clues: Row clues for phase 2 (erasing)
            phase2_col_clues: Column clues for phase 2 (erasing)
            
        Returns:
            Tuple of (success, solved_grid) where solved_grid uses string encoding
        """
        # Solve Phase 1
        success1, phase1_grid = self.solve_nonogram(phase1_row_clues, phase1_col_clues)
        if not success1:
            # Return empty grid if Phase 1 fails
            empty_grid = [['-' for _ in range(self.width)] for _ in range(self.height)]
            return False, empty_grid
        
        # Solve Phase 2
        success2, phase2_grid = self.solve_nonogram(phase2_row_clues, phase2_col_clues)
        if not success2:
            # Return Phase 1 only if Phase 2 fails
            result_grid = [['1' if cell else '-' for cell in row] for row in phase1_grid]
            return False, result_grid
        
        # Combine both phases into the string format
        result_grid = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                phase1_filled = phase1_grid[r][c]
                phase2_filled = phase2_grid[r][c]
                
                if phase1_filled and phase2_filled:
                    row.append('X')  # Both phases
                elif phase1_filled:
                    row.append('1')  # Phase 1 only
                elif phase2_filled:
                    row.append('2')  # Phase 2 only
                else:
                    row.append('-')  # Neither phase
            result_grid.append(row)
        
        return True, result_grid