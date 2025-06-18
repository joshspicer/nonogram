#!/usr/bin/env python3
"""
Test script to verify TypeScript implementation matches Python implementation
"""
import json
import subprocess
import os
from squared_away import parse_grid, generate_shading_clues, generate_erasing_clues

def test_file(filename):
    """Test compatibility between Python and TypeScript implementations for a given file"""
    print(f"Testing {filename}...")
    
    # Get Python results
    with open(filename, 'r') as f:
        grid_str = f.read()
    
    grid = parse_grid(grid_str)
    py_shading_rows, py_shading_cols = generate_shading_clues(grid)
    py_erasing_rows, py_erasing_cols = generate_erasing_clues(grid)
    
    # Get TypeScript results (parse from its output)
    try:
        result = subprocess.run(['npx', 'ts-node', 'src/index.ts', filename], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            print(f"  ERROR: TypeScript failed with: {result.stderr}")
            return False
            
        # Extract the JSON arrays from TypeScript output
        lines = result.stdout.split('\n')
        ts_shading_rows = None
        ts_shading_cols = None  
        ts_erasing_rows = None
        ts_erasing_cols = None
        
        for line in lines:
            if line.startswith('Rows: '):
                if ts_shading_rows is None:
                    ts_shading_rows = json.loads(line[6:])
                else:
                    ts_erasing_rows = json.loads(line[6:])
            elif line.startswith('Cols: '):
                if ts_shading_cols is None:
                    ts_shading_cols = json.loads(line[6:])
                else:
                    ts_erasing_cols = json.loads(line[6:])
        
        # Compare results
        if (py_shading_rows == ts_shading_rows and 
            py_shading_cols == ts_shading_cols and
            py_erasing_rows == ts_erasing_rows and
            py_erasing_cols == ts_erasing_cols):
            print(f"  ✅ PASS: Results match")
            return True
        else:
            print(f"  ❌ FAIL: Results differ")
            print(f"    Python shading rows: {py_shading_rows}")
            print(f"    TypeScript shading rows: {ts_shading_rows}")
            return False
            
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    """Run compatibility tests"""
    print("Squared Away Nonogram Generator - Compatibility Test")
    print("==================================================")
    
    test_files = ['nonogram_puzzle_1.txt', 'nonogram_puzzle_2.txt']
    if os.path.exists('v2-puzzle/96squared.txt'):
        test_files.append('v2-puzzle/96squared.txt')
    
    passed = 0
    total = len(test_files)
    
    for filename in test_files:
        if os.path.exists(filename):
            if test_file(filename):
                passed += 1
        else:
            print(f"Skipping {filename} (not found)")
            total -= 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TypeScript implementation matches Python.")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    exit(main())