# Squared Away Nonogram Generator (TypeScript)

This is a TypeScript implementation of the Squared Away Nonogram Generator, ported from the original Python version.

## Features
- Parses a nonogram grid from a text file
- Generates phase 1 (shading) and phase 2 (erasing) clues for rows and columns
- Prints the grid and clues to the console

## Usage

1. Install dependencies:
   ```sh
   npm install
   ```
2. Run the program with a puzzle file:
   ```sh
   npx ts-node src/index.ts nonogram_puzzle_1.txt
   ```

## Example Puzzle File
```
-1-2
1X2-
-1--
2-1X
```

## Output Example
```
Grid:
- 1 - 2
1 X 2 -
- 1 - -
2 - 1 X

Shading Clues (Rows): [ [ 1, 1 ], [ 2 ], [ 1 ], [ 1, 1 ] ]
Shading Clues (Cols): [ [ 1, 1 ], [ 2 ], [ 1 ], [ 1, 1 ] ]
Erasing Clues (Rows): [ [ 1 ], [ 1, 1 ], [ 0 ], [ 1, 1 ] ]
Erasing Clues (Cols): [ [ 1 ], [ 1, 1 ], [ 1 ], [ 1, 1 ] ]
```

---

This implementation is a starting point and can be extended with visualization or editor features in the future.
