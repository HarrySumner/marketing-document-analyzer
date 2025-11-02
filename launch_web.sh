#!/bin/bash

echo "========================================"
echo "Multi-Agent Research Assistant"
echo "Web Interface Launcher"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "Checking Python version..."
python3 --version

echo ""
echo "Installing/updating dependencies..."
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo ""
echo "========================================"
echo "Starting Web Interface..."
echo "========================================"
echo ""
echo "The interface will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "To share with colleagues on your network, use:"
echo "the Network URL shown below"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 -m streamlit run app.py
