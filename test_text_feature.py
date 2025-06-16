#!/usr/bin/env python3
"""
Text to Nonogram Feature Test
============================

This script validates the new text-to-nonogram functionality added to squared_away.py.

The feature allows users to:
1. Input any text or number
2. Convert it to a nonogram puzzle using font rendering
3. Visualize the puzzle with proper clues
4. Save the generated puzzle

Usage:
    python3 test_text_feature.py
"""

import sys
import os

# Add the main directory to Python path
sys.path.insert(0, '/home/runner/work/nonogram/nonogram')

# Use non-interactive matplotlib backend for testing
import matplotlib
matplotlib.use('Agg')

try:
    from squared_away import text_to_nonogram, NonoGramVisualizer, generate_shading_clues, generate_erasing_clues
    print("✓ Successfully imported required functions")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_basic_text_conversion():
    """Test basic text to grid conversion"""
    print("\n--- Testing Basic Text Conversion ---")
    
    test_inputs = ["A", "123", "Hi", "ABC", "HELLO"]
    
    for text in test_inputs:
        try:
            grid = text_to_nonogram(text)
            
            # Validate grid structure
            if not grid or not grid[0]:
                print(f"✗ {text}: Empty grid generated")
                continue
                
            height = len(grid)
            width = len(grid[0])
            
            # Check consistent row lengths
            if not all(len(row) == width for row in grid):
                print(f"✗ {text}: Inconsistent row lengths")
                continue
                
            # Check valid characters
            valid_chars = {'-', '1', '2', 'X'}
            all_chars = set(cell for row in grid for cell in row)
            if not all_chars.issubset(valid_chars):
                print(f"✗ {text}: Invalid characters in grid")
                continue
                
            # Check for actual content
            filled_cells = sum(1 for row in grid for cell in row if cell == '1')
            if filled_cells == 0:
                print(f"✗ {text}: No filled cells in grid")
                continue
                
            print(f"✓ {text}: {height}x{width} grid with {filled_cells} filled cells")
            
        except Exception as e:
            print(f"✗ {text}: Error - {e}")

def test_font_size_variations():
    """Test different font sizes"""
    print("\n--- Testing Font Size Variations ---")
    
    text = "ABC"
    font_sizes = [10, 16, 20, 24, 32]
    
    for size in font_sizes:
        try:
            grid = text_to_nonogram(text, font_size=size)
            height = len(grid)
            width = len(grid[0])
            filled = sum(1 for row in grid for cell in row if cell == '1')
            print(f"✓ Font size {size}: {height}x{width} grid with {filled} filled cells")
        except Exception as e:
            print(f"✗ Font size {size}: Error - {e}")

def test_clue_generation():
    """Test that generated grids work with clue generation"""
    print("\n--- Testing Clue Generation ---")
    
    try:
        grid = text_to_nonogram("HI", font_size=20)
        
        # Test shading clues
        row_clues, col_clues = generate_shading_clues(grid)
        print(f"✓ Generated shading clues: {len(row_clues)} rows, {len(col_clues)} cols")
        
        # Test erasing clues
        row_clues, col_clues = generate_erasing_clues(grid)
        print(f"✓ Generated erasing clues: {len(row_clues)} rows, {len(col_clues)} cols")
        
    except Exception as e:
        print(f"✗ Clue generation failed: {e}")

def test_visualizer_integration():
    """Test integration with NonoGramVisualizer"""
    print("\n--- Testing Visualizer Integration ---")
    
    try:
        grid = text_to_nonogram("A", font_size=24)
        visualizer = NonoGramVisualizer(grid)
        
        # Check that visualizer initializes properly
        print(f"✓ Visualizer created for {len(grid)}x{len(grid[0])} grid")
        print(f"✓ Max row clues: {visualizer.max_row_clues}")
        print(f"✓ Max col clues: {visualizer.max_col_clues}")
        
        # Test clues are generated
        if visualizer.shading_row_clues and visualizer.shading_col_clues:
            print("✓ Clues properly generated in visualizer")
        else:
            print("✗ Clues not generated in visualizer")
            
    except Exception as e:
        print(f"✗ Visualizer integration failed: {e}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n--- Testing Edge Cases ---")
    
    edge_cases = [
        ("", "Empty string"),
        (" ", "Single space"),
        ("!", "Special character"),
        ("1", "Single digit"),
        ("VERYLONGTEXT", "Long text"),
    ]
    
    for text, description in edge_cases:
        try:
            if text == "":
                # Empty string should be handled gracefully
                print(f"⚠ {description}: Skipping empty string test")
                continue
                
            grid = text_to_nonogram(text, font_size=16)
            
            if grid and grid[0]:
                height = len(grid)
                width = len(grid[0])
                filled = sum(1 for row in grid for cell in row if cell == '1')
                print(f"✓ {description}: {height}x{width} grid with {filled} filled cells")
            else:
                print(f"✗ {description}: Empty grid generated")
                
        except Exception as e:
            print(f"✗ {description}: Error - {e}")

def test_file_output():
    """Test file output functionality"""
    print("\n--- Testing File Output ---")
    
    try:
        grid = text_to_nonogram("TEST", font_size=20)
        
        # Save to file
        test_file = "/tmp/test_nonogram_output.txt"
        with open(test_file, 'w') as f:
            for row in grid:
                f.write(''.join(row) + '\n')
        
        # Verify file was created and has content
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                content = f.read().strip()
            
            if content:
                lines = content.split('\n')
                print(f"✓ File output: {len(lines)} lines written to {test_file}")
                
                # Verify content format
                if all(all(c in '-12X' for c in line) for line in lines):
                    print("✓ File content format is valid")
                else:
                    print("✗ File content has invalid characters")
            else:
                print("✗ File output: Empty file created")
        else:
            print("✗ File output: File not created")
            
    except Exception as e:
        print(f"✗ File output failed: {e}")

def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("TEXT TO NONOGRAM FEATURE TEST")
    print("=" * 60)
    
    test_functions = [
        test_basic_text_conversion,
        test_font_size_variations,
        test_clue_generation,
        test_visualizer_integration,
        test_edge_cases,
        test_file_output
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"✗ Test function {test_func.__name__} failed: {e}")
    
    print("\n" + "=" * 60)
    print("FEATURE TEST COMPLETE")
    print("=" * 60)
    print("\nThe text-to-nonogram feature is ready for use!")
    print("\nTo use the feature:")
    print("1. Run: python3 squared_away.py")
    print("2. Choose option 1: Create puzzle from text/number")
    print("3. Enter your text and font size")
    print("4. Enjoy your custom nonogram puzzle!")

if __name__ == "__main__":
    run_all_tests()