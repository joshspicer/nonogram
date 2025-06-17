# Squared Away Nonogram Generator - Go Version

A Go implementation of the Squared Away Nonogram Generator, featuring two-phase nonogram puzzles with text-based visualization.

## Overview

This Go version replicates the core functionality of the Python nonogram application, providing:

- **Phase 1**: Shading clues (standard nonogram rules)
- **Phase 2**: Erasing clues (standard nonogram rules, but grid starts filled and clues indicate cells to erase)
- Text-based visualization with Unicode symbols
- Interactive editor mode
- File I/O compatibility with the Python version

## Features

### ✅ Core Functionality
- Parse nonogram grids from text files
- Generate Phase 1 (shading) and Phase 2 (erasing) clues
- Text-based visualization with three phases:
  - Phase 0: Empty grid with clues
  - Phase 1: Show shaded cells
  - Phase 2: Show final state with erased cells
- Interactive editor mode for creating puzzles
- Save puzzles to text files

### ✅ File Format Compatibility
Compatible with the existing Python version file format:
- `1` = Phase 1 (shading) only
- `2` = Phase 2 (erasing) only  
- `X` = Both phases (shade then erase)
- `-` = Empty cell

## Installation

### Prerequisites
- Go 1.21 or later

### Build
```bash
go build -o nonogram main.go
```

## Usage

### View Existing Puzzles
```bash
# View a puzzle file with interactive phase navigation
./nonogram < nonogram_puzzle_1.txt

# Or using redirection
cat nonogram_puzzle_1.txt | ./nonogram
```

### Create New Puzzles (Editor Mode)
```bash
# Start interactive editor
./nonogram

# Follow prompts:
# 1. Enter width (e.g., 5)
# 2. Enter height (e.g., 5) 
# 3. Use coordinates to mark cells
# 4. Advance through phases
# 5. Save your puzzle
```

### Editor Commands
- `row,col` - Toggle cell at coordinates (1-indexed)
- `next` - Advance from Phase 1 to Phase 2
- `save filename.txt` - Save puzzle to file
- `quit` - Exit editor

### Example Editor Session
```
Enter puzzle width: 3
Enter puzzle height: 3

Phase 1: Shading Mode
Enter coordinates (row,col), 'next', 'save <file>', or 'quit': 1,1
Enter coordinates (row,col), 'next', 'save <file>', or 'quit': 2,2  
Enter coordinates (row,col), 'next', 'save <file>', or 'quit': next

Phase 2: Erasing Mode
Enter coordinates (row,col), 'save <file>', or 'quit': 1,3
Enter coordinates (row,col), 'save <file>', or 'quit': save my_puzzle.txt
```

## Visualization Legend

| Symbol | Meaning |
|--------|---------|
| `█` | Filled cell |
| `░` | Erased cell |
| `·` | Empty cell |

## File Format

Puzzles are stored as text files with one character per cell:

```
XXX-XXX-XXX-X1X
X---2-X-2-X-X-X
X---2-X-2-X-X-X
XXX-X1X-XXX-XXX
2-X-2-X-X-2---X
2-X-2-X-X-2---X
XXX-XXX-XXX-11X
```

## Differences from Python Version

### Text-Based Interface
- Uses Unicode characters instead of matplotlib graphics
- Terminal-based interaction instead of GUI
- Sequential phase viewing instead of real-time switching

### Maintained Compatibility
- ✅ Same file format
- ✅ Same clue generation algorithms  
- ✅ Same grid representations
- ✅ Same puzzle logic

### Simplified Features
- Text-based visualization (no matplotlib dependency)
- Command-line editor (no mouse interaction)
- Sequential viewing (no real-time phase switching)

## Testing

Run the test suite:
```bash
./test.sh
```

Tests verify:
- File input processing
- Build process
- Editor mode functionality
- Compatibility with existing puzzle files

## Examples

The Go version works with all existing puzzle files:
- `nonogram_puzzle_1.txt`
- `nonogram_puzzle_2.txt`  
- `v2-puzzle/96squared.txt`

## Performance

The Go version offers:
- Fast startup time
- Low memory usage
- No external dependencies
- Cross-platform compatibility

## Contributing

The Go implementation maintains the same core algorithms as the Python version while providing a lightweight, dependency-free alternative for terminal environments.