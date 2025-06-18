import * as fs from 'fs';
import * as path from 'path';

// Parse the input grid string into a 2D array
function parseGrid(gridStr: string): string[][] {
  const lines = gridStr.trim().split('\n').filter(line => line.trim().length > 0);
  if (lines.length === 0) {
    throw new Error('Empty grid provided');
  }
  
  const grid = lines.map(line => line.trim().split(''));
  
  // Validate grid dimensions
  const expectedWidth = grid[0].length;
  for (let i = 0; i < grid.length; i++) {
    if (grid[i].length !== expectedWidth) {
      throw new Error(`Row ${i + 1} has ${grid[i].length} cells, expected ${expectedWidth}`);
    }
  }
  
  // Validate cell contents
  const validCells = new Set(['-', '1', '2', 'X']);
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      if (!validCells.has(grid[i][j])) {
        throw new Error(`Invalid cell '${grid[i][j]}' at row ${i + 1}, column ${j + 1}. Valid cells are: -, 1, 2, X`);
      }
    }
  }
  
  return grid;
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
function printNonogram(grid: string[][], outputFile?: string) {
  const [shadingRows, shadingCols] = generateShadingClues(grid);
  const [erasingRows, erasingCols] = generateErasingClues(grid);

  const output: string[] = [];
  
  output.push('Squared Away Nonogram Generator');
  output.push('================================');
  output.push('');
  output.push('Grid:');
  for (const row of grid) {
    output.push(row.join(' '));
  }
  output.push('');
  output.push('Phase 1 - Shading Clues:');
  output.push(`Rows: ${JSON.stringify(shadingRows)}`);
  output.push(`Cols: ${JSON.stringify(shadingCols)}`);
  output.push('');
  output.push('Phase 2 - Erasing Clues:');
  output.push(`Rows: ${JSON.stringify(erasingRows)}`);
  output.push(`Cols: ${JSON.stringify(erasingCols)}`);
  
  const outputText = output.join('\n');
  
  if (outputFile) {
    try {
      fs.writeFileSync(outputFile, outputText, 'utf-8');
      console.log(`Results saved to ${outputFile}`);
    } catch (error) {
      console.error(`Error saving to file: ${error}`);
      process.exit(1);
    }
  } else {
    console.log(outputText);
  }
}

// Show usage information
function showUsage() {
  console.log('Squared Away Nonogram Generator - TypeScript Edition');
  console.log('===================================================');
  console.log('');
  console.log('Usage:');
  console.log('  npx ts-node src/index.ts <input_file> [output_file]');
  console.log('  npm start <input_file> [output_file]');
  console.log('');
  console.log('Arguments:');
  console.log('  input_file   - Text file containing the nonogram grid');
  console.log('  output_file  - Optional output file (results printed to console if not specified)');
  console.log('');
  console.log('Grid Format:');
  console.log('  -  Empty cell');
  console.log('  1  Phase 1 shading cell');
  console.log('  2  Phase 2 erasing cell');
  console.log('  X  Both phase 1 and phase 2 cell');
  console.log('');
  console.log('Example grid file:');
  console.log('  X1X-X2X');
  console.log('  2-X-1-X');
  console.log('  XXX-XXX');
}

// Main entry point
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showUsage();
    process.exit(args.length === 0 ? 1 : 0);
  }

  const inputFile = args[0];
  const outputFile = args[1];

  try {
    // Check if input file exists
    if (!fs.existsSync(inputFile)) {
      console.error(`Error: Input file '${inputFile}' not found`);
      process.exit(1);
    }

    // Read and validate the grid
    const gridStr = fs.readFileSync(inputFile, 'utf-8');
    if (!gridStr.trim()) {
      console.error('Error: Input file is empty');
      process.exit(1);
    }

    const grid = parseGrid(gridStr);
    printNonogram(grid, outputFile);
    
  } catch (error) {
    if (error instanceof Error) {
      console.error(`Error: ${error.message}`);
    } else {
      console.error('An unexpected error occurred');
    }
    process.exit(1);
  }
}

main();
