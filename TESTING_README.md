# Testing Guide for Squared Away Nonogram Generator

This project includes a comprehensive unit test suite that validates all core functionality of the nonogram generator.

## Running the Tests

### Method 1: Using the test runner script
```bash
python3 run_tests.py
```

### Method 2: Running tests directly
```bash
python3 test_squared_away.py
```

### Method 3: Using Python's unittest module
```bash
python3 -m unittest test_squared_away.py -v
```

## Test Coverage

The test suite covers the following components:

### Core Functions
- **`parse_grid()`** - Grid parsing from string input
- **`generate_shading_clues()`** - Phase 1 (shading) clue generation
- **`generate_erasing_clues()`** - Phase 2 (erasing) clue generation
- **`create_empty_grid()`** - Empty grid creation

### NonoGramVisualizer Class
- **Initialization** - Constructor and setup
- **Clue generation** - Automatic clue calculation
- **Editor mode** - Interactive editing functionality
- **Phase management** - Phase cycling and transitions

### Integration Tests
- **Real puzzle files** - Tests with existing nonogram_puzzle_*.txt files
- **File I/O** - Loading and parsing actual puzzle data
- **End-to-end workflows** - Complete puzzle processing pipelines

### Edge Cases
- **Empty inputs** - Handling of empty strings and grids
- **Irregular grids** - Grids with uneven row lengths
- **Unknown characters** - Handling of unexpected input characters
- **Boundary conditions** - Single cell grids, zero-size grids

## Test Statistics

- **Total Test Cases**: 33
- **Test Classes**: 8
- **Functions Tested**: 6 core functions + visualizer methods
- **Coverage Areas**: Parsing, clue generation, grid creation, visualization, edge cases

## Test Results

When all tests pass, you should see:

```
----------------------------------------------------------------------
Ran 33 tests in 0.004s

OK
```

## Adding New Tests

To add new test cases:

1. **For new functions**: Add a new test class inheriting from `unittest.TestCase`
2. **For existing functions**: Add new test methods to the appropriate existing test class
3. **Naming convention**: Test methods should start with `test_` and have descriptive names
4. **Documentation**: Include docstrings explaining what each test validates

Example:
```python
def test_new_functionality(self):
    """Test description of what this validates."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = squared_away.function_to_test(input_data)
    
    # Assert
    expected = "expected output"
    self.assertEqual(result, expected)
```

## Continuous Integration

These tests are designed to be run automatically in CI/CD pipelines. The test runner script returns appropriate exit codes:
- **0**: All tests passed
- **1**: Some tests failed

This allows for automated testing and quality assurance in development workflows.