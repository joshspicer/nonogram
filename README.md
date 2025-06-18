# Squared Away Nonogram Generator (TypeScript)

This is a TypeScript implementation of the Squared Away Nonogram Generator, ported from the original Python version. It provides a robust command-line interface for processing nonogram grids and generating clues.

## Features
- Parses nonogram grids from text files with comprehensive validation
- Generates phase 1 (shading) and phase 2 (erasing) clues for rows and columns
- Prints results to console or saves to file
- Comprehensive error handling and input validation
- Command-line help and usage information
- 100% compatibility with the Python implementation

## Installation

1. Install dependencies:
   ```sh
   npm install
   ```

## Usage

### Basic Usage
```sh
# Using npm script
npm run nonogram <puzzle_file.txt>

# Using ts-node directly  
npx ts-node src/index.ts <puzzle_file.txt>

# Save results to file
npm run nonogram <puzzle_file.txt> <output_file.txt>
```

### Getting Help
```sh
npm run nonogram --help
```

## Grid Format

Nonogram grids use the following characters:
- `-` : Empty cell
- `1` : Phase 1 shading cell  
- `2` : Phase 2 erasing cell
- `X` : Both phase 1 and phase 2 cell

## Example

### Input File (`example.txt`)
```
X1X-X2X
2-X-1-X
XXX-XXX
```

### Command
```sh
npm run nonogram example.txt
```

### Output
```
Squared Away Nonogram Generator
================================

Grid:
X 1 X - X 2 X
2 - X - 1 - X
X X X - X X X

Phase 1 - Shading Clues:
Rows: [[3],[1,1,1],[3]]
Cols: [[1,1,1],[1],[3],[0],[1,1,1],[1],[3]]

Phase 2 - Erasing Clues:
Rows: [[1,1,1],[1,1,1],[3,3]]
Cols: [[3],[1],[3],[0],[1,1],[1,1],[3]]
```

## Testing

Run the compatibility test to verify the TypeScript implementation matches the Python version:

```sh
python3 test_compatibility.py
```

## Build

To compile the TypeScript code:

```sh
npm run build
```

This creates compiled JavaScript files in the `dist/` directory.

---

This TypeScript implementation provides the core functionality of the Squared Away Nonogram Generator in a robust, well-tested command-line tool.
