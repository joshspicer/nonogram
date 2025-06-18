package main

import (
	"reflect"
	"testing"
)

func TestParseGrid(t *testing.T) {
	input := "X1X\n-2-\n1X2"
	expected := Grid{
		{'X', '1', 'X'},
		{'-', '2', '-'},
		{'1', 'X', '2'},
	}
	
	result := parseGrid(input)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("parseGrid() = %v, want %v", result, expected)
	}
}

func TestGenerateShadingClues(t *testing.T) {
	grid := Grid{
		{'X', '1', '-'},
		{'-', '-', '1'},
		{'1', 'X', '1'},
	}
	
	expectedRowClues := [][]int{
		{2},    // X1 = 2 consecutive
		{1},    // single 1
		{3},    // 1X1 = 3 consecutive (1 and X are both phase 1)
	}
	expectedColClues := [][]int{
		{1, 1}, // X in row 1, 1 in row 3
		{1, 1}, // 1 in row 1, X in row 3  
		{2},    // 1 in row 2, 1 in row 3 = 2 consecutive
	}
	
	rowClues, colClues := generateShadingClues(grid)
	
	if !reflect.DeepEqual(rowClues, expectedRowClues) {
		t.Errorf("generateShadingClues() rowClues = %v, want %v", rowClues, expectedRowClues)
	}
	if !reflect.DeepEqual(colClues, expectedColClues) {
		t.Errorf("generateShadingClues() colClues = %v, want %v", colClues, expectedColClues)
	}
}

func TestGenerateErasingClues(t *testing.T) {
	grid := Grid{
		{'X', '2', '-'},
		{'-', '-', '2'},
		{'2', 'X', '2'},
	}
	
	expectedRowClues := [][]int{
		{2},    // X2 = 2 consecutive  
		{1},    // single 2
		{3},    // 2X2 = 3 consecutive (2 and X are both phase 2)
	}
	expectedColClues := [][]int{
		{1, 1}, // X in row 1, 2 in row 3
		{1, 1}, // 2 in row 1, X in row 3
		{2},    // 2 in row 2, 2 in row 3 = 2 consecutive
	}
	
	rowClues, colClues := generateErasingClues(grid)
	
	if !reflect.DeepEqual(rowClues, expectedRowClues) {
		t.Errorf("generateErasingClues() rowClues = %v, want %v", rowClues, expectedRowClues)
	}
	if !reflect.DeepEqual(colClues, expectedColClues) {
		t.Errorf("generateErasingClues() colClues = %v, want %v", colClues, expectedColClues)
	}
}

func TestCreateEmptyGrid(t *testing.T) {
	width, height := 3, 2
	expected := Grid{
		{'-', '-', '-'},
		{'-', '-', '-'},
	}
	
	result := createEmptyGrid(width, height)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("createEmptyGrid() = %v, want %v", result, expected)
	}
}

func TestFormatClues(t *testing.T) {
	clues := []int{1, 2, 3}
	expected := "1 2 3"
	
	result := formatClues(clues)
	if result != expected {
		t.Errorf("formatClues() = %v, want %v", result, expected)
	}
}