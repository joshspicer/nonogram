import * as fs from 'fs';

// Parse the input grid string into a 2D array
function parseGrid(gridStr: string): string[][] {
  return gridStr.trim().split('\n').map(line => line.trim().split(''));
}

// Generate phase 1 shading clues for rows and columns
function generateShadingClues(grid: string[][]): [number[][], number[][]] {
  const rowClues: number[][] = grid.map(row => {
    const clues: number[] = [];
    let count = 0;
    for (const cell of row) {
      if (cell === '1' || cell === 'X') count++;
      else if (count > 0) { clues.push(count); count = 0; }
    }
    if (count > 0) clues.push(count);
    return clues.length ? clues : [0];
  });

  const colClues: number[][] = [];
  for (let col = 0; col < grid[0].length; col++) {
    let clues: number[] = [];
    let count = 0;
    for (let row = 0; row < grid.length; row++) {
      const cell = grid[row][col];
      if (cell === '1' || cell === 'X') count++;
      else if (count > 0) { clues.push(count); count = 0; }
    }
    if (count > 0) clues.push(count);
    colClues.push(clues.length ? clues : [0]);
  }
  return [rowClues, colClues];
}

// Generate phase 2 erasing clues for rows and columns
function generateErasingClues(grid: string[][]): [number[][], number[][]] {
  const rowClues: number[][] = grid.map(row => {
    const clues: number[] = [];
    let count = 0;
    for (const cell of row) {
      if (cell === '2' || cell === 'X') count++;
      else if (count > 0) { clues.push(count); count = 0; }
    }
    if (count > 0) clues.push(count);
    return clues.length ? clues : [0];
  });

  const colClues: number[][] = [];
  for (let col = 0; col < grid[0].length; col++) {
    let clues: number[] = [];
    let count = 0;
    for (let row = 0; row < grid.length; row++) {
      const cell = grid[row][col];
      if (cell === '2' || cell === 'X') count++;
      else if (count > 0) { clues.push(count); count = 0; }
    }
    if (count > 0) clues.push(count);
    colClues.push(clues.length ? clues : [0]);
  }
  return [rowClues, colClues];
}

// Print the grid and clues to the console
function printNonogram(grid: string[][]) {
  const [shadingRows, shadingCols] = generateShadingClues(grid);
  const [erasingRows, erasingCols] = generateErasingClues(grid);

  console.log('Grid:');
  for (const row of grid) {
    console.log(row.join(' '));
  }
  console.log('\nShading Clues (Rows):', shadingRows);
  console.log('Shading Clues (Cols):', shadingCols);
  console.log('Erasing Clues (Rows):', erasingRows);
  console.log('Erasing Clues (Cols):', erasingCols);
}

// Main entry point
function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: ts-node src/index.ts <puzzle_file.txt>');
    process.exit(1);
  }
  const gridStr = fs.readFileSync(file, 'utf-8');
  const grid = parseGrid(gridStr);
  printNonogram(grid);
}

main();
