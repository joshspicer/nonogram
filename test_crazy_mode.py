#!/usr/bin/env python3
"""
Simple test script to verify crazy mode functionality
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from squared_away import NonoGramVisualizer, parse_grid

def test_basic_functionality():
    """Test that basic functionality still works"""
    test_grid_str = """X1X-X2X
2-X-1-X
22X-11X"""
    
    grid = parse_grid(test_grid_str)
    
    # Test normal mode
    print("Testing normal mode...")
    visualizer = NonoGramVisualizer(grid, editor_mode=False, crazy_mode=False)
    assert visualizer.crazy_mode == False
    assert len(visualizer.phases) == 3
    assert "Initial Grid" in visualizer.phases[0]
    print("✓ Normal mode initialized successfully")
    
    # Test crazy mode
    print("Testing crazy mode...")
    crazy_visualizer = NonoGramVisualizer(grid, editor_mode=False, crazy_mode=True)
    assert crazy_visualizer.crazy_mode == True
    assert len(crazy_visualizer.phases) == 3
    assert "🌪️" in crazy_visualizer.phases[0]  # Check for crazy mode phase names
    assert hasattr(crazy_visualizer, 'crazy_colors')
    assert hasattr(crazy_visualizer, 'crazy_patterns')
    assert hasattr(crazy_visualizer, 'animation_counter')
    print("✓ Crazy mode initialized successfully")
    
    # Test editor mode with crazy mode
    print("Testing crazy editor mode...")
    crazy_editor = NonoGramVisualizer(grid, editor_mode=True, crazy_mode=True)
    assert crazy_editor.editor_mode == True
    assert crazy_editor.crazy_mode == True
    print("✓ Crazy editor mode initialized successfully")
    
    print("All tests passed! 🎉")

if __name__ == "__main__":
    test_basic_functionality()