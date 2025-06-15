#!/bin/bash
# QoE Analysis Pipeline
# This script runs the entire QoE analysis pipeline:
# 1. Downloads the data from the Google Sheet
# 2. Analyzes the data and generates visualizations

# Set up error handling
set -e

echo "===== QoE Analysis Pipeline ====="
echo "Starting analysis at $(date)"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import sys; sys.exit(0 if all(map(lambda m: m in sys.modules or __import__(m), ['pandas', 'matplotlib', 'seaborn', 'numpy', 'requests'])) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Create output directory
OUTPUT_DIR="visualizations"
mkdir -p "$OUTPUT_DIR"

# Step 1: Download the data
echo
echo "Step 1: Downloading data from Google Sheet..."
python3 download_qoe_data.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to download data"
    exit 1
fi

# Step 2: Analyze the data
echo
echo "Step 2: Analyzing data and generating visualizations..."
python3 analyze_qoe_data.py --csv qoe_data.csv --output "$OUTPUT_DIR"
if [ $? -ne 0 ]; then
    echo "Error: Failed to analyze data"
    exit 1
fi

echo
echo "Analysis completed successfully!"
echo "Visualizations are available in the '$OUTPUT_DIR' directory"
echo

# List generated visualizations
echo "Generated visualizations:"
ls -1 "$OUTPUT_DIR"/*.png | sed 's/^/- /'

echo
echo "To view the visualizations, open the files in your preferred image viewer"
echo "For example: open $OUTPUT_DIR/overall_accuracy.png"
