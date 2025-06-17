# 3D Nonogram Example

This is an example 3D nonogram puzzle file. The format uses blank lines to separate layers in the z-direction.

## Format
```
Layer 0:
1X1
X-X  
1X1

Layer 1:
-2-
2-2
-2-

Layer 2:
X1X
1-1
X1X
```

## Cell Types
- `1` = Phase 1 shading cell
- `2` = Phase 2 erasing cell  
- `X` = Both phase 1 and phase 2 cell
- `-` = Empty cell

## Usage
To view this 3D puzzle:
```bash
python3 squared_away.py < example_3d_puzzle.txt
```

## Navigation
- Press ENTER to cycle through phases
- Press UP/DOWN arrow keys to navigate between layers
- In editor mode, click on cubes to edit them