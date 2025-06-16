# Text-to-Nonogram Feature

This feature allows you to convert any text or number into a nonogram puzzle using font rendering.

## How to Use

1. Run the main program:
   ```bash
   python3 squared_away.py
   ```

2. Choose option 1: "Create puzzle from text/number"

3. Enter your text or number when prompted

4. Optionally specify a font size (default is 20)

5. Choose whether to save the generated grid to a file

6. The nonogram puzzle will be displayed with proper clues

## Examples

- **Text**: "HELLO" → Creates a nonogram puzzle spelling out "HELLO"
- **Numbers**: "2024" → Creates a nonogram puzzle showing "2024"
- **Single letters**: "A" → Creates a nonogram puzzle of the letter "A"

## Technical Details

- Uses PIL (Pillow) for font rendering
- Converts text to bitmap and then to nonogram grid format
- Automatically crops empty space around the text
- Supports different font sizes for various puzzle complexities
- Generates standard nonogram clues for the resulting puzzle

## Grid Format

- `-` represents empty cells
- `1` represents filled cells (to be shaded in the puzzle)
- Compatible with existing nonogram visualization system

## Font Sizes

- **Small (10-16)**: Compact puzzles, good for short text
- **Medium (18-24)**: Standard readable puzzles
- **Large (28+)**: Detailed puzzles with more complexity

The feature automatically handles font scaling and ensures the generated puzzles are solvable and visually appealing.