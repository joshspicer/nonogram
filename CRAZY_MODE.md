# Crazy Mode Documentation

## Overview

Crazy Mode is an experimental feature for the Squared Away Nonogram Generator that introduces unconventional, visually intense, and creative effects to the nonogram solving experience.

## How to Enable Crazy Mode

### Command Line
```bash
# Long flag
python squared_away.py --crazy < puzzle.txt

# Short flag  
python squared_away.py -c < puzzle.txt

# Editor mode with crazy mode
python squared_away.py --crazy
```

### In Code
```python
from squared_away import NonoGramVisualizer

# Enable crazy mode
visualizer = NonoGramVisualizer(grid, crazy_mode=True)
```

## What Crazy Mode Does

### Visual Effects
- **Random Colors**: Grid lines, cells, and text use vibrant, randomly selected colors
- **Dynamic Patterns**: Cell patterns change with each redraw using various hatching styles
- **Animated Elements**: Visual elements change over time with animation counters
- **Rotated Text**: Clue numbers are randomly rotated for a chaotic look
- **Dark Theme**: Uses a dark background theme for dramatic effect

### Creative Phase Names
Instead of standard phase names, crazy mode uses:
- 🌪️ Reality Distortion Field
- 🎨 Chromatic Chaos Protocol  
- 🌈 Psychedelic Refinement Matrix

### Interactive Elements
- Special crazy mode instructions and warnings
- Enhanced visual feedback during editing
- Unpredictable visual behavior with each interaction

## Warnings and Considerations

⚠️ **WARNING**: Crazy mode may cause:
- Visually intense or distracting effects
- Unpredictable behavior with each use
- Not suitable for serious puzzle solving
- Rapid color changes that might affect users with photosensitivity

## Examples

### Basic Usage
```bash
# View a puzzle in crazy mode
python squared_away.py --crazy < nonogram_puzzle_1.txt

# Create a puzzle in crazy mode
python squared_away.py -c
```

### Expected Behavior
- Grid lines appear in random colors and styles
- Cells fill with vibrant, random patterns
- Text appears at random angles and colors
- Background uses dark theme
- Phase names are creative and unconventional
- Each redraw produces different visual effects

## Technical Details

### New Features Added
- `--crazy` / `-c` command line flags
- `crazy_mode` parameter in `NonoGramVisualizer` class
- Random color palettes and pattern sets
- Animation counter for dynamic effects
- Enhanced visual feedback system

### Code Changes
- Added argparse for command line handling
- Extended visualizer with crazy mode logic
- Preserved all existing functionality
- Added comprehensive help documentation

## Compatibility

Crazy mode is fully compatible with:
- All existing puzzle formats
- Editor mode functionality
- Normal mode operation (when disabled)
- Standard nonogram features

The feature is designed to be additive - enabling crazy mode does not break any existing functionality.