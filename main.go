package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

// Grid represents a 2D nonogram grid
type Grid [][]rune

// parseGrid parses the input grid string into a 2D Grid
func parseGrid(gridStr string) Grid {
	lines := strings.Split(strings.TrimSpace(gridStr), "\n")
	grid := make(Grid, len(lines))
	
	for i, line := range lines {
		grid[i] = []rune(strings.TrimSpace(line))
	}
	
	return grid
}

// generateShadingClues generates the phase 1 shading clues for rows and columns.
// Cells marked as '1' or 'X' are part of Phase 1 solution.
func generateShadingClues(grid Grid) ([][]int, [][]int) {
	if len(grid) == 0 || len(grid[0]) == 0 {
		return nil, nil
	}
	
	height := len(grid)
	width := len(grid[0])
	
	// Row clues
	rowClues := make([][]int, height)
	for i, row := range grid {
		clues := []int{}
		count := 0
		
		for _, cell := range row {
			if cell == '1' || cell == 'X' { // Cells to be shaded in Phase 1
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
			if cell == '1' || cell == 'X' { // Cells to be shaded in Phase 1
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

// generateErasingClues generates the phase 2 erasing clues for rows and columns.
// Cells marked as '2' or 'X' are to be erased in Phase 2.
func generateErasingClues(grid Grid) ([][]int, [][]int) {
	if len(grid) == 0 || len(grid[0]) == 0 {
		return nil, nil
	}
	
	height := len(grid)
	width := len(grid[0])
	
	// Row clues
	rowClues := make([][]int, height)
	for i, row := range grid {
		clues := []int{}
		count := 0
		
		for _, cell := range row {
			if cell == '2' || cell == 'X' { // Cells to be erased in Phase 2
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
			if cell == '2' || cell == 'X' { // Cells to be erased in Phase 2
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

// formatClues formats a slice of integers as a space-separated string
func formatClues(clues []int) string {
	strs := make([]string, len(clues))
	for i, clue := range clues {
		strs[i] = strconv.Itoa(clue)
	}
	return strings.Join(strs, " ")
}

// processNonogram processes the nonogram grid and prints the clues
func processNonogram(gridStr string) {
	grid := parseGrid(gridStr)
	
	if len(grid) == 0 {
		fmt.Println("Error: empty grid")
		return
	}
	
	fmt.Println("Squared Away Nonogram Generator (Go)")
	fmt.Printf("Grid size: %dx%d\n\n", len(grid[0]), len(grid))
	
	// Generate clues
	shadingRowClues, shadingColClues := generateShadingClues(grid)
	erasingRowClues, erasingColClues := generateErasingClues(grid)
	
	// Print Phase 1 (Shading) clues
	fmt.Println("Phase 1 - Shading Clues:")
	fmt.Println("Row clues:")
	for i, clues := range shadingRowClues {
		fmt.Printf("  Row %d: %s\n", i+1, formatClues(clues))
	}
	
	fmt.Println("Column clues:")
	for i, clues := range shadingColClues {
		fmt.Printf("  Col %d: %s\n", i+1, formatClues(clues))
	}
	
	// Print Phase 2 (Erasing) clues
	fmt.Println("\nPhase 2 - Erasing Clues:")
	fmt.Println("Row clues:")
	for i, clues := range erasingRowClues {
		fmt.Printf("  Row %d: %s\n", i+1, formatClues(clues))
	}
	
	fmt.Println("Column clues:")
	for i, clues := range erasingColClues {
		fmt.Printf("  Col %d: %s\n", i+1, formatClues(clues))
	}
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

// isATTY checks if stdin is connected to a terminal
func isATTY() bool {
	stat, err := os.Stdin.Stat()
	if err != nil {
		return false
	}
	return (stat.Mode() & os.ModeCharDevice) != 0
}

func main() {
	fmt.Println("Squared Away Nonogram Generator (Go)")
	
	// Check if input is from a file/pipe or keyboard
	if !isATTY() {
		// Reading from file or pipe
		input, err := io.ReadAll(os.Stdin)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading input: %v\n", err)
			os.Exit(1)
		}
		processNonogram(string(input))
	} else {
		// Interactive mode - create empty grid
		reader := bufio.NewReader(os.Stdin)
		
		fmt.Print("Enter puzzle width: ")
		widthStr, err := reader.ReadString('\n')
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading width: %v\n", err)
			os.Exit(1)
		}
		width, err := strconv.Atoi(strings.TrimSpace(widthStr))
		if err != nil || width <= 0 {
			fmt.Println("Please enter a valid positive integer for width")
			os.Exit(1)
		}
		
		fmt.Print("Enter puzzle height: ")
		heightStr, err := reader.ReadString('\n')
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading height: %v\n", err)
			os.Exit(1)
		}
		height, err := strconv.Atoi(strings.TrimSpace(heightStr))
		if err != nil || height <= 0 {
			fmt.Println("Please enter a valid positive integer for height")
			os.Exit(1)
		}
		
		// Create empty grid and show format
		grid := createEmptyGrid(width, height)
		fmt.Printf("\nEmpty %dx%d grid created.\n", width, height)
		fmt.Println("Grid format:")
		for _, row := range grid {
			fmt.Println(string(row))
		}
		
		fmt.Println("\nTo use this grid:")
		fmt.Println("- Save the grid to a file")
		fmt.Println("- Edit the file: '-' = empty, '1' = phase 1, '2' = phase 2, 'X' = both phases")
		fmt.Println("- Run: go run main.go < your_file.txt")
	}
}