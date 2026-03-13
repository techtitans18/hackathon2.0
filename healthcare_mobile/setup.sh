#!/bin/bash

echo "========================================"
echo "Healthcare Mobile App - Quick Setup"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "Step 4: Creating cache directory..."
mkdir -p cache
echo "✓ Cache directory created"
echo ""

echo "Step 5: Creating temp directory..."
mkdir -p temp
echo "✓ Temp directory created"
echo ""

echo "========================================"
echo "Setup Complete! 🎉"
echo "========================================"
echo ""
echo "To run the app:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python main.py"
echo ""
echo "To build for Android:"
echo "  buildozer -v android debug"
echo ""
echo "For more information, see README.md"
echo ""
