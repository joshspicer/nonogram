# Squared Away Nonogram Generator

This repository contains implementations of a two-phase nonogram puzzle generator in both Python and Go.

## Overview

The program generates clues for a unique two-phase nonogram puzzle:
- **Phase 1**: Shading clues (standard nonogram rules)
- **Phase 2**: Erasing clues (standard nonogram rules, but the entire grid is filled to start and the clues indicate erasing)

## Grid Format

The grid uses the following character encoding:
- `-` = empty cell
- `1` = Phase 1 shading only
- `2` = Phase 2 erasing only  
- `X` = Both Phase 1 shading and Phase 2 erasing

## Python Implementation

### Requirements
```bash
pip install matplotlib numpy
```

### Usage
```bash
# Process a puzzle file
python squared_away.py < puzzle_file.txt

# Interactive editor mode
python squared_away.py
```

The Python version includes a full GUI with matplotlib for creating and visualizing puzzles.

## Go Implementation

### Requirements
- Go 1.16 or later

### Usage

#### Build the program
```bash
go build -o nonogram main.go
```

#### Process a puzzle file
```bash
./nonogram < puzzle_file.txt
# or
go run main.go < puzzle_file.txt
```

#### Interactive mode
```bash
./nonogram
# or  
go run main.go
```

#### Run tests
```bash
go test -v
```

### Example Output
```
Squared Away Nonogram Generator (Go)
Grid size: 15x7

Phase 1 - Shading Clues:
Row clues:
  Row 1: 3 1 1 3 3
  Row 2: 1 1 1 1 1
  ...

Phase 2 - Erasing Clues:
Row clues:
  Row 1: 1 1 3 3 3
  Row 2: 1 1 1 1 1
  ...
```

## Example Puzzle Files

The repository includes example puzzle files:
- `nonogram_puzzle_1.txt`
- `nonogram_puzzle_2.txt`

These demonstrate the grid format and can be used to test both implementations.

## Development

### Go Project Structure
- `main.go` - Core implementation
- `main_test.go` - Unit tests
- `go.mod` - Go module file

### Key Functions
- `parseGrid()` - Parse grid string into 2D array
- `generateShadingClues()` - Generate Phase 1 clues
- `generateErasingClues()` - Generate Phase 2 clues
- `processNonogram()` - Main processing function

The Go implementation focuses on the core nonogram logic and provides a command-line interface, while the Python version includes advanced visualization and editing capabilities.