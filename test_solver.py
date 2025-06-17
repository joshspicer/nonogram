#!/usr/bin/env python3
"""
Test script for the Nonogram AI Solver
"""

import sys
import os

# Add the current directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nonogram_solver import NonogramSolver
from squared_away import generate_shading_clues, generate_erasing_clues, parse_grid


def test_basic_solver():
    """Test the solver with a simple 3x3 nonogram."""
    print("Testing basic solver with a simple 3x3 puzzle...")
    
    # Create a simple test puzzle
    # Pattern:
    # T-T
    # ---  
    # T-T
    solver = NonogramSolver(3, 3)
    
    row_clues = [[1, 1], [0], [1, 1]]  # Row clues: [1,1], 0, [1,1]
    col_clues = [[2], [0], [2]]        # Column clues: 2, 0, 2
    
    success, grid = solver.solve_nonogram(row_clues, col_clues)
    
    print(f"Success: {success}")
    print("Solved grid:")
    for row in grid:
        print(['X' if cell else '-' for cell in row])
    
    expected = [[True, False, True], [False, False, False], [True, False, True]]
    if grid == expected:
        print("✅ Basic solver test passed!")
        return True
    else:
        print("❌ Basic solver test failed!")
        print(f"Expected: {expected}")
        print(f"Got: {grid}")
        return False


def test_two_phase_solver():
    """Test the two-phase solver with the provided puzzle."""
    print("\nTesting two-phase solver with example puzzle...")
    
    # Load the example puzzle
    try:
        with open('nonogram_puzzle_1.txt', 'r') as f:
            grid_str = f.read()
    except FileNotFoundError:
        print("❌ Test puzzle file not found!")
        return False
    
    # Parse the grid
    original_grid = parse_grid(grid_str)
    print("Original puzzle:")
    for row in original_grid:
        print(''.join(row))
    
    # Generate clues
    phase1_row_clues, phase1_col_clues = generate_shading_clues(original_grid)
    phase2_row_clues, phase2_col_clues = generate_erasing_clues(original_grid)
    
    print(f"Phase 1 row clues: {phase1_row_clues}")
    print(f"Phase 1 col clues: {phase1_col_clues}")
    print(f"Phase 2 row clues: {phase2_row_clues}")
    print(f"Phase 2 col clues: {phase2_col_clues}")
    
    # Solve the puzzle
    height = len(original_grid)
    width = len(original_grid[0])
    solver = NonogramSolver(width, height)
    
    success, solved_grid = solver.solve_two_phase_nonogram(
        phase1_row_clues, phase1_col_clues,
        phase2_row_clues, phase2_col_clues
    )
    
    print(f"Success: {success}")
    print("Solved grid:")
    for row in solved_grid:
        print(''.join(row))
    
    # Compare with original (should match)
    if solved_grid == original_grid:
        print("✅ Two-phase solver test passed!")
        return True
    else:
        print("❌ Two-phase solver test failed!")
        print("Expected vs Got:")
        for i, (orig_row, solved_row) in enumerate(zip(original_grid, solved_grid)):
            orig_str = ''.join(orig_row)
            solved_str = ''.join(solved_row)
            status = "✅" if orig_str == solved_str else "❌"
            print(f"Row {i}: {orig_str} -> {solved_str} {status}")
        return False


def test_line_solver():
    """Test the line solving algorithm."""
    print("\nTesting line solver...")
    
    solver = NonogramSolver(5, 1)  # Just for accessing the line solver
    
    # Test case 1: Simple line with clue [3]
    clues = [3]
    line = [None, None, None, None, None]
    result = solver.solve_line(clues, line)
    print(f"Clues: {clues}, Line: {line}")
    print(f"Result: {result}")
    
    # Only the middle cell (index 2) should be determined (True) since it appears in all arrangements
    expected = [None, None, True, None, None]
    if result == expected:
        print("✅ Line solver test 1 passed!")
        test1_passed = True
    else:
        print(f"❌ Line solver test 1 failed! Expected: {expected}")
        test1_passed = False
    
    # Test case 2: Line with clue [1, 1]
    clues = [1, 1]
    line = [None, None, None, None, None]
    result = solver.solve_line(clues, line)
    print(f"Clues: {clues}, Line: {line}")
    print(f"Result: {result}")
    
    # Test case 3: No clues (empty line)
    clues = [0]
    line = [None, None, None]
    result = solver.solve_line(clues, line)
    expected = [False, False, False]
    print(f"Clues: {clues}, Line: {line}")
    print(f"Result: {result}")
    
    if result == expected:
        print("✅ Line solver test 3 passed!")
        return test1_passed  # Return test1 result since that was the main concern
    else:
        print(f"❌ Line solver test 3 failed! Expected: {expected}")
        return False


def main():
    """Run all tests."""
    print("Running Nonogram Solver Tests")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_line_solver():
        tests_passed += 1
    
    if test_basic_solver():
        tests_passed += 1
    
    if test_two_phase_solver():
        tests_passed += 1
    
    print(f"\nTests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    main()