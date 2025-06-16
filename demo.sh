#!/bin/bash

echo "=== Squared Away Nonogram Generator - Crazy Mode Demonstration ==="
echo ""

echo "📋 Normal Mode:"
echo "python squared_away.py < nonogram_puzzle_1.txt"
echo ""

echo "🎪 Crazy Mode:"  
echo "python squared_away.py --crazy < nonogram_puzzle_1.txt"
echo ""

echo "🎨 Crazy Mode (short flag):"
echo "python squared_away.py -c < nonogram_puzzle_1.txt"
echo ""

echo "📝 Editor Mode (normal):"
echo "echo '5\n5' | python squared_away.py"
echo ""

echo "🚀 Editor Mode (crazy):"
echo "echo '5\n5' | python squared_away.py --crazy"
echo ""

echo "❓ Help:"
echo "python squared_away.py --help"
echo ""

echo "Testing help command:"
python3 squared_away.py --help