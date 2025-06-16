# CGSynth Video Quality Evaluation Tool

A web-based tool for conducting video quality evaluation studies, specifically designed for comparing different video processing techniques.

## Overview

This project provides a complete solution for conducting video quality evaluation studies where participants compare pairs of videos and rate their quality. The system ensures consistent and reproducible results by using deterministic algorithms for video pair selection based on user IDs.

The project also includes tools for analyzing the collected data, extracting insights from the Google Sheet responses, and generating visualizations to compare when users correctly identified synthetic videos versus when they didn't. The analysis pipeline can be run with a single command, making it easy to generate insights from the collected data.

## Features

- **User Management**: Each participant gets a unique, persistent user ID
- **Deterministic Pairing**: Reproducible video pair selection using seeded randomization
- **Responsive Design**: Works on both desktop and mobile devices
- **Data Collection**: Records user ratings and additional feedback
- **Offline-First**: Works without an internet connection after initial load
- **Version Control**: Tracks video list versions and hashes for data integrity
- **Data Analysis**: Comprehensive analysis tools with visualization generation
- **Reproducibility**: Ability to retrieve exact video pairs shown to specific users
- **Sample Data Generation**: Tools to generate sample data for testing without accessing the Google Sheet

## Project Structure

### Website Components
- `index.html` - Main web interface for the evaluation tool
- `generate_video_list.py` - Script to generate a list of videos with versioning
- `retrieve_videos_from_user_hash_id.py` - Tool to reproduce exact video pairs shown to a user
- `video_list.json` - Configuration file listing all available videos
- `videos/` - Directory containing video files for evaluation
- `AppsScript/` - Google Apps Script for data collection (if using Google Sheets)

### Analysis Tools
- `download_qoe_data.py` - Downloads the data from the Google Sheet and saves it as a CSV file
- `analyze_qoe_data.py` - Analyzes the data and generates visualizations for accuracy metrics
- `generate_sample_data.py` - Generates sample data for testing the analysis without accessing the Google Sheet
- `run_analysis.sh` - Shell script to run the entire analysis pipeline in one command
- `requirements.txt` - List of Python package dependencies for the analysis tools
- `visualizations/` - Directory containing generated visualization outputs:
  - `overall_accuracy.png` - Bar chart showing the proportion of correct vs. incorrect guesses
  - `accuracy_by_type.png` - Bar chart showing the accuracy for different video type combinations
  - `confusion_matrix.png` - Heatmap showing the relationship between reality and user guesses
  - `user_accuracy_distribution.png` - Histogram showing the distribution of accuracy across users

## Getting Started

### Prerequisites

- Python 3.6+
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- (Optional) Google account if using Google Sheets for data collection

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cgreplay_demo.git
   cd cgreplay_demo
   ```

2. Place your video files in the `videos/` directory

3. Generate the video list:
   ```bash
   python3 generate_video_list.py
   ```
   This will create/update `video_list.json` with all videos found in the `videos/` directory.

### Running the Application

1. Start a local web server. For example, using Python's built-in server:
   ```bash
   python3 -m http.server 8000
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

### For Participants

1. Open the evaluation tool in your web browser
2. You'll be assigned a unique user ID (or can enter an existing one)
3. Follow the on-screen instructions to evaluate video pairs
4. For each pair, rate the quality difference between the two videos
5. Complete any additional questions
6. Submit your evaluation when finished

### For Researchers

To retrieve the exact video pairs shown to a specific user:

```bash
python3 retrieve_videos_from_user_hash_id.py USER_ID
```

This will output the list of video pairs that were shown to that user, allowing for result verification and analysis.

Additional options for the retrieval script:
```bash
# Output in CSV format
python3 retrieve_videos_from_user_hash_id.py USER_ID --csv

# Save output to a file
python3 retrieve_videos_from_user_hash_id.py USER_ID --save user_pairs.csv

# Generate pairs algorithmically instead of using CSV data
python3 retrieve_videos_from_user_hash_id.py USER_ID --generate
```

The script first attempts to load pairs directly from the QoE data CSV file. If no data is found or the `--generate` flag is used, it falls back to algorithmic generation using the same deterministic algorithm as the frontend.

## Data Collection

By default, the application logs evaluation data to the browser's console. To enable Google Sheets integration:

1. Create a new Google Sheet
2. Go to Extensions > Apps Script
3. Copy the contents of `AppsScript/webserver_connection_cgreplay_yes.gs` into the script editor
4. Deploy the script as a web app
5. Update the `SCRIPT_URL` in `index.html` with your web app URL

## Customization

### Adding New Videos

1. Place new video files in the `videos/` directory
2. Run `generate_video_list.py` to update the video list
3. The new videos will be included in the next evaluation session

### Modifying Questions

Edit the HTML form in `index.html` to add, remove, or modify the evaluation questions.

## Troubleshooting

- **Videos not loading**: Check the browser's developer console for errors
- **Data not submitting**: Verify the Google Apps Script is properly deployed and the URL is correct
- **Inconsistent pairs**: Ensure the same video list version is used for both evaluation and retrieval

## License

[Specify your license here]

## Acknowledgments

- Built with standard web technologies (HTML, CSS, JavaScript)
- Uses a custom implementation of a seeded random number generator for reproducibility
- Designed for academic and research use in video quality assessment studies

## Data Analysis

The project includes tools for analyzing the subjective Quality of Experience (QoE) assessment data collected in the Google Sheet.

### Prerequisites

Before running the analysis scripts, you need to have Python 3.6+ installed. You can install all required packages using:

```bash
pip install -r requirements.txt
```

This will install:
- pandas
- matplotlib
- seaborn
- numpy
- requests
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

### Running the Analysis

#### Option 1: Run the Complete Pipeline (Recommended)

The easiest way to run the analysis is to use the provided shell script:

```bash
./run_analysis.sh
```

This script will:
1. Check for required dependencies and install them if needed
2. Download the data from the Google Sheet
3. Analyze the data and generate visualizations
4. Display a summary of the generated visualizations

#### Option 2: Run Steps Individually

If you prefer to run the steps individually:

1. Download the data:
   ```bash
   python download_qoe_data.py
   ```

2. Analyze the data:
   ```bash
   python analyze_qoe_data.py --csv qoe_data.csv
   ```

#### Alternative: Using Sample Data

If you want to test the analysis without accessing the Google Sheet, you can generate sample data:

```bash
python generate_sample_data.py
python analyze_qoe_data.py --csv sample_qoe_data.csv
```

### Visualizations

The analysis generates the following visualizations in the `visualizations` directory:

1. **Overall Accuracy**: Bar chart showing the proportion of correct vs. incorrect guesses
2. **Accuracy by Video Type**: Bar chart showing the accuracy for different video type combinations
3. **Confusion Matrix**: Heatmap showing the relationship between reality and user guesses
4. **User Accuracy Distribution**: Histogram showing the distribution of accuracy across users

### How the Analysis Works

The analysis script:

1. Classifies videos as synthetic or real based on their filenames:
   - Videos with "interpolated" in the name are considered synthetic
   - Videos with "original" in the name are considered real
   - Videos with "degrad" in the name are considered synthetic
   - Other videos default to real

2. Determines the "reality" for each video pair and compares it with the user's guess

3. Calculates various metrics including:
   - Overall accuracy (proportion of correct identifications)
   - Accuracy by video type (how well users identify different combinations of real/synthetic videos)
   - User accuracy distribution (histogram showing how accuracy varies across users)
   - Confusion matrix (relationship between actual reality and user guesses)

4. Generates visualizations to help interpret the results and identify patterns in user perception
