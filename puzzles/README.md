# Nonogram Puzzles

This directory contains nonogram puzzles organized by difficulty level.

## Difficulty Levels

### Easy (5x5 grids)
Simple patterns with clear, continuous lines. Perfect for beginners.
- **Simple Cross**: Basic cross pattern
- **Letter L**: L-shaped pattern
- **Square**: Hollow square outline

### Medium (7x15 or 9x9 grids)
More complex patterns with multiple segments and strategic thinking required.
- **Diamond**: Diamond pattern with strategic placement
- **Puzzle 1**: Multi-phase nonogram with shading and erasing
- **Puzzle 2**: Advanced pattern recognition

### Hard (15x19 grids)
Complex patterns requiring advanced logical reasoning and pattern recognition.
- **96Squared**: Complex multi-phase puzzle
- **Complex Pattern**: Large grid with intricate design

## File Format

Puzzles are stored as text files where:
- `1` represents cells to be shaded in Phase 1
- `2` represents cells to be erased in Phase 2  
- `X` represents cells that appear in both phases
- `-` represents empty cells

## Adding New Puzzles

To add a new puzzle:
1. Create a `.txt` file in the appropriate difficulty folder
2. Use the format described above
3. Test the puzzle using the editor mode to verify clues are generated correctly