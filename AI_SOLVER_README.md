# Nonogram AI Solver

This repository now includes a complete AI solver for nonogram puzzles, with support for the unique two-phase nonogram format used in the Squared Away application.

## Features

- **Complete Nonogram Solver**: Uses constraint propagation and backtracking algorithms
- **Two-Phase Support**: Handles both Phase 1 (shading) and Phase 2 (erasing) puzzles
- **Multiple Interfaces**: Command-line and interactive GUI modes
- **High Success Rate**: Successfully solves all provided puzzle examples

## Usage

### Command Line Interface

#### Interactive GUI Mode
```bash
python squared_away.py --solve puzzle.txt
```
This opens the puzzle in the visualizer where you can press ENTER or 'S' to start solving.

#### Headless CLI Mode
```bash
python squared_away.py --solve --headless puzzle.txt
```
This solves the puzzle and prints the result without opening a GUI.

#### Pipe Input
```bash
cat puzzle.txt | python squared_away.py --solve --headless
```

### Options

- `--solve` or `-s`: Enable AI solver mode
- `--headless` or `-h`: Run without GUI (command-line only)

## Puzzle Format

The solver supports the two-phase nonogram format:

- `'-'`: Empty cell
- `'1'`: Cell shaded in Phase 1 only
- `'2'`: Cell erased in Phase 2 only  
- `'X'`: Cell shaded in Phase 1 AND erased in Phase 2

## Algorithm

The solver uses a combination of:

1. **Line Solving**: Processes each row and column individually using constraint satisfaction
2. **Arrangement Generation**: Generates all valid arrangements for given clues
3. **Constraint Propagation**: Iteratively applies line solving until no more progress is made
4. **Backtracking**: For difficult puzzles, tries different values and recursively solves

## Testing

Run the test suite to verify the solver:

```bash
python test_solver.py
```

The tests include:
- Line solver algorithm verification
- Basic 3x3 puzzle solving
- Complex two-phase puzzle solving

## Examples

### Example 1: Solving a puzzle file
```bash
$ python squared_away.py --solve --headless nonogram_puzzle_1.txt
Squared Away Nonogram Generator
AI Solver mode enabled
Solving puzzle...
Original puzzle:
X1X-X2X-XXX-XXX
2-X-1-X-1-2-2-1
22X-11X-1-2-2-1
11X---X-XXX-XXX
--X---X-2-1-X-2
--X---X-2-1-X-2
11X---X-XXX-XXX

Phase 1 row clues: [[3, 1, 1, 3, 3], [1, 1, 1, 1, 1], ...]
Phase 1 col clues: [[1, 1, 1], [1, 1, 1], [7], [0], ...]
Phase 2 row clues: [[1, 1, 3, 3, 3], [1, 1, 1, 1, 1], ...]
Phase 2 col clues: [[3], [1], [7], [0], ...]

✅ Puzzle solved successfully!
Solved puzzle:
X1X-X2X-XXX-XXX
2-X-1-X-1-2-2-1
22X-11X-1-2-2-1
11X---X-XXX-XXX
--X---X-2-1-X-2
--X---X-2-1-X-2
11X---X-XXX-XXX
```

## Implementation Details

The AI solver is implemented in `nonogram_solver.py` and integrated into the main application `squared_away.py`. The solver class `NonogramSolver` provides methods for:

- `solve_nonogram()`: Solves standard single-phase nonograms
- `solve_two_phase_nonogram()`: Solves two-phase puzzles
- `solve_line()`: Core line-solving algorithm
- Various helper methods for arrangement generation and validation

The integration adds minimal changes to the existing codebase while providing powerful solving capabilities for both simple and complex nonogram puzzles.