#!/bin/bash

# Test script for Go nonogram implementation

echo "Testing Go Nonogram Implementation"
echo "=================================="

# Test 1: File input mode with puzzle 1
echo -e "\n1. Testing file input with nonogram_puzzle_1.txt..."
echo "y" | ./nonogram < nonogram_puzzle_1.txt > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ File input test 1 passed"
else
    echo "✗ File input test 1 failed"
fi

# Test 2: File input mode with puzzle 2  
echo -e "\n2. Testing file input with nonogram_puzzle_2.txt..."
echo "y" | ./nonogram < nonogram_puzzle_2.txt > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ File input test 2 passed"
else
    echo "✗ File input test 2 failed"
fi

# Test 3: Build test
echo -e "\n3. Testing build..."
go build -o nonogram_test main.go
if [ $? -eq 0 ]; then
    echo "✓ Build test passed"
    rm nonogram_test
else
    echo "✗ Build test failed"
fi

echo -e "\n4. Testing editor mode creation (5x5 grid)..."
echo -e "5\n5\nquit" | ./nonogram > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Editor mode test passed"
else
    echo "✗ Editor mode test failed"
fi

echo -e "\nAll tests completed!"