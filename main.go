package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Grid represents a nonogram grid using runes
type Grid [][]rune

// Nonogram represents a complete nonogram puzzle
type Nonogram struct {
	Grid           Grid
	Width          int
	Height         int
	ShadingRowClues [][]int
	ShadingColClues [][]int
	ErasingRowClues [][]int
	ErasingColClues [][]int
}

// parseGrid converts input string to a Grid
func parseGrid(input string) Grid {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	grid := make(Grid, len(lines))
	
	for i, line := range lines {
		line = strings.TrimSpace(line)
		grid[i] = []rune(line)
	}
	
	return grid
}

// generateShadingClues generates phase 1 clues for rows and columns
// Cells marked as '1' or 'X' are part of Phase 1 solution
func generateShadingClues(grid Grid) ([][]int, [][]int) {
	height := len(grid)
	width := len(grid[0])
	
	// Row clues
	rowClues := make([][]int, height)
	for i, row := range grid {
		clues := []int{}
		count := 0
		
		for _, cell := range row {
			if cell == '1' || cell == 'X' {
				count++
			} else if count > 0 {
				clues = append(clues, count)
				count = 0
			}
		}
		
		if count > 0 {
			clues = append(clues, count)
		}
		
		if len(clues) == 0 {
			clues = append(clues, 0)
		}
		
		rowClues[i] = clues
	}
	
	// Column clues
	colClues := make([][]int, width)
	for j := 0; j < width; j++ {
		clues := []int{}
		count := 0
		
		for i := 0; i < height; i++ {
			cell := grid[i][j]
			if cell == '1' || cell == 'X' {
				count++
			} else if count > 0 {
				clues = append(clues, count)
				count = 0
			}
		}
		
		if count > 0 {
			clues = append(clues, count)
		}
		
		if len(clues) == 0 {
			clues = append(clues, 0)
		}
		
		colClues[j] = clues
	}
	
	return rowClues, colClues
}

// generateErasingClues generates phase 2 clues for rows and columns
// Cells marked as '2' or 'X' are to be erased in Phase 2
func generateErasingClues(grid Grid) ([][]int, [][]int) {
	height := len(grid)
	width := len(grid[0])
	
	// Row clues
	rowClues := make([][]int, height)
	for i, row := range grid {
		clues := []int{}
		count := 0
		
		for _, cell := range row {
			if cell == '2' || cell == 'X' {
				count++
			} else if count > 0 {
				clues = append(clues, count)
				count = 0
			}
		}
		
		if count > 0 {
			clues = append(clues, count)
		}
		
		if len(clues) == 0 {
			clues = append(clues, 0)
		}
		
		rowClues[i] = clues
	}
	
	// Column clues
	colClues := make([][]int, width)
	for j := 0; j < width; j++ {
		clues := []int{}
		count := 0
		
		for i := 0; i < height; i++ {
			cell := grid[i][j]
			if cell == '2' || cell == 'X' {
				count++
			} else if count > 0 {
				clues = append(clues, count)
				count = 0
			}
		}
		
		if count > 0 {
			clues = append(clues, count)
		}
		
		if len(clues) == 0 {
			clues = append(clues, 0)
		}
		
		colClues[j] = clues
	}
	
	return rowClues, colClues
}

// NewNonogram creates a new Nonogram from a grid
func NewNonogram(grid Grid) *Nonogram {
	height := len(grid)
	width := len(grid[0])
	
	shadingRowClues, shadingColClues := generateShadingClues(grid)
	erasingRowClues, erasingColClues := generateErasingClues(grid)
	
	return &Nonogram{
		Grid:            grid,
		Width:           width,
		Height:          height,
		ShadingRowClues: shadingRowClues,
		ShadingColClues: shadingColClues,
		ErasingRowClues: erasingRowClues,
		ErasingColClues: erasingColClues,
	}
}

// formatClues converts clue slice to string representation
func formatClues(clues []int) string {
	if len(clues) == 1 && clues[0] == 0 {
		return "0"
	}
	
	strs := make([]string, len(clues))
	for i, clue := range clues {
		strs[i] = strconv.Itoa(clue)
	}
	return strings.Join(strs, " ")
}

// displayPuzzle shows the puzzle in text format with clues
func (n *Nonogram) displayPuzzle(phase int) {
	fmt.Println("\n" + strings.Repeat("=", 50))
	switch phase {
	case 0:
		fmt.Println("Phase 0: Initial Grid (Empty)")
	case 1:
		fmt.Println("Phase 1: Apply Foundation Protocol")
	case 2:
		fmt.Println("Phase 2: Execute Refinement Protocol")
	}
	fmt.Println(strings.Repeat("=", 50))
	
	// Calculate max clue widths for formatting
	maxRowClueWidth := 0
	for _, clues := range n.ShadingRowClues {
		width := len(formatClues(clues))
		if width > maxRowClueWidth {
			maxRowClueWidth = width
		}
	}
	
	// Display column clues
	fmt.Print(strings.Repeat(" ", maxRowClueWidth+2))
	for j := 0; j < n.Width; j++ {
		shadingClues := formatClues(n.ShadingColClues[j])
		fmt.Printf("%3s", shadingClues)
	}
	fmt.Println()
	
	// Display column erasing clues if not all zeros
	hasErasingColClues := false
	for _, clues := range n.ErasingColClues {
		if !(len(clues) == 1 && clues[0] == 0) {
			hasErasingColClues = true
			break
		}
	}
	
	if hasErasingColClues {
		fmt.Print(strings.Repeat(" ", maxRowClueWidth+2))
		for j := 0; j < n.Width; j++ {
			erasingClues := formatClues(n.ErasingColClues[j])
			if erasingClues != "0" {
				fmt.Printf("%3s", "("+erasingClues+")")
			} else {
				fmt.Printf("%3s", "")
			}
		}
		fmt.Println()
	}
	
	fmt.Println()
	
	// Display grid with row clues
	for i := 0; i < n.Height; i++ {
		// Row shading clues
		shadingClues := formatClues(n.ShadingRowClues[i])
		fmt.Printf("%*s │", maxRowClueWidth, shadingClues)
		
		// Grid cells
		for j := 0; j < n.Width; j++ {
			cell := n.Grid[i][j]
			symbol := " "
			
			switch phase {
			case 0:
				// Empty grid
				symbol = "·"
			case 1:
				// Phase 1: show shaded cells
				if cell == '1' || cell == 'X' {
					symbol = "█"
				} else {
					symbol = "·"
				}
			case 2:
				// Phase 2: show all filled, then erased cells
				if cell == '2' || cell == 'X' {
					symbol = "░" // Erased cells
				} else {
					symbol = "█" // Filled cells
				}
			}
			
			fmt.Printf(" %s ", symbol)
		}
		
		// Row erasing clues
		erasingClues := formatClues(n.ErasingRowClues[i])
		if erasingClues != "0" {
			fmt.Printf(" │ (%s)", erasingClues)
		}
		
		fmt.Println()
	}
	
	fmt.Println()
	fmt.Println("Legend: █ = Filled, ░ = Erased, · = Empty")
	fmt.Println("Clues in parentheses are for Phase 2 (erasing)")
}

// createEmptyGrid creates an empty grid with specified dimensions
func createEmptyGrid(width, height int) Grid {
	grid := make(Grid, height)
	for i := range grid {
		grid[i] = make([]rune, width)
		for j := range grid[i] {
			grid[i][j] = '-'
		}
	}
	return grid
}

// saveGrid saves the grid to a file
func (n *Nonogram) saveGrid(filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()
	
	for _, row := range n.Grid {
		fmt.Fprintln(file, string(row))
	}
	
	return nil
}

// editorMode provides a simple text-based editor
func editorMode(width, height int) {
	grid := createEmptyGrid(width, height)
	nonogram := NewNonogram(grid)
	
	phase := 1 // Start with phase 1 (shading)
	
	fmt.Println("\nNonogram Editor Mode")
	fmt.Println("====================")
	fmt.Printf("Creating %dx%d grid\n", width, height)
	fmt.Println("\nInstructions:")
	fmt.Println("- Enter coordinates as 'row,col' (1-indexed)")
	fmt.Println("- Phase 1: Mark cells for shading")
	fmt.Println("- Phase 2: Mark cells for erasing")
	fmt.Println("- Commands: 'next' (next phase), 'save <filename>', 'quit'")
	
	scanner := bufio.NewScanner(os.Stdin)
	
	for {
		// Display current state
		nonogram.displayPuzzle(phase)
		
		if phase == 1 {
			fmt.Println("\nPhase 1: Shading Mode")
			fmt.Print("Enter coordinates (row,col), 'next', 'save <file>', or 'quit': ")
		} else {
			fmt.Println("\nPhase 2: Erasing Mode")
			fmt.Print("Enter coordinates (row,col), 'save <file>', or 'quit': ")
		}
		
		if !scanner.Scan() {
			break
		}
		
		input := strings.TrimSpace(scanner.Text())
		
		if input == "quit" {
			break
		}
		
		if input == "next" && phase == 1 {
			phase = 2
			nonogram = NewNonogram(grid) // Regenerate clues
			continue
		}
		
		if strings.HasPrefix(input, "save ") {
			filename := strings.TrimSpace(input[5:])
			if filename == "" {
				filename = "nonogram_puzzle.txt"
			}
			err := nonogram.saveGrid(filename)
			if err != nil {
				fmt.Printf("Error saving file: %v\n", err)
			} else {
				fmt.Printf("Puzzle saved to %s\n", filename)
				break
			}
			continue
		}
		
		// Parse coordinates
		parts := strings.Split(input, ",")
		if len(parts) != 2 {
			fmt.Println("Invalid input. Use format: row,col")
			continue
		}
		
		row, err1 := strconv.Atoi(strings.TrimSpace(parts[0]))
		col, err2 := strconv.Atoi(strings.TrimSpace(parts[1]))
		
		if err1 != nil || err2 != nil {
			fmt.Println("Invalid coordinates. Use numbers only.")
			continue
		}
		
		// Convert to 0-indexed
		row--
		col--
		
		if row < 0 || row >= height || col < 0 || col >= width {
			fmt.Printf("Coordinates out of bounds. Use 1-%d for rows, 1-%d for cols.\n", height, width)
			continue
		}
		
		// Toggle cell based on phase
		if phase == 1 {
			if grid[row][col] == '-' {
				grid[row][col] = '1'
			} else {
				grid[row][col] = '-'
			}
		} else {
			current := grid[row][col]
			switch current {
			case '-':
				grid[row][col] = '2'
			case '1':
				grid[row][col] = 'X' // Both phase 1 and 2
			case 'X':
				grid[row][col] = '1' // Back to just phase 1
			case '2':
				grid[row][col] = '-' // Back to empty
			}
		}
		
		// Regenerate clues
		nonogram = NewNonogram(grid)
	}
	
	if scanner.Err() != nil {
		fmt.Printf("Error reading input: %v\n", scanner.Err())
	}
}

func main() {
	fmt.Println("Squared Away Nonogram Generator (Go Version)")
	fmt.Println("============================================")
	
	// Check if input is from stdin (file/pipe)
	stat, _ := os.Stdin.Stat()
	if (stat.Mode() & os.ModeCharDevice) == 0 {
		// Reading from pipe/file
		scanner := bufio.NewScanner(os.Stdin)
		var input strings.Builder
		
		for scanner.Scan() {
			input.WriteString(scanner.Text() + "\n")
		}
		
		if scanner.Err() != nil {
			fmt.Printf("Error reading input: %v\n", scanner.Err())
			os.Exit(1)
		}
		
		grid := parseGrid(input.String())
		nonogram := NewNonogram(grid)
		
		// Display all phases
		for phase := 0; phase <= 2; phase++ {
			nonogram.displayPuzzle(phase)
			if phase < 2 {
				fmt.Println("\nPress Enter to continue to next phase...")
				bufio.NewReader(os.Stdin).ReadBytes('\n')
			}
		}
	} else {
		// Interactive editor mode
		fmt.Print("Enter puzzle width: ")
		scanner := bufio.NewScanner(os.Stdin)
		scanner.Scan()
		width, err := strconv.Atoi(strings.TrimSpace(scanner.Text()))
		if err != nil || width <= 0 {
			fmt.Println("Invalid width. Please enter a positive integer.")
			os.Exit(1)
		}
		
		fmt.Print("Enter puzzle height: ")
		scanner.Scan()
		height, err := strconv.Atoi(strings.TrimSpace(scanner.Text()))
		if err != nil || height <= 0 {
			fmt.Println("Invalid height. Please enter a positive integer.")
			os.Exit(1)
		}
		
		editorMode(width, height)
	}
}