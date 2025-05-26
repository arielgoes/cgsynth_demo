# CGSynth Video Quality Evaluation Tool

A web-based tool for conducting video quality evaluation studies, specifically designed for comparing different video processing techniques.

## Overview

This project provides a complete solution for conducting video quality evaluation studies where participants compare pairs of videos and rate their quality. The system ensures consistent and reproducible results by using deterministic algorithms for video pair selection based on user IDs.

## Features

- **User Management**: Each participant gets a unique, persistent user ID
- **Deterministic Pairing**: Reproducible video pair selection using seeded randomization
- **Responsive Design**: Works on both desktop and mobile devices
- **Data Collection**: Records user ratings and additional feedback
- **Offline-First**: Works without an internet connection after initial load
- **Version Control**: Tracks video list versions and hashes for data integrity

## Project Structure

- `index.html` - Main web interface for the evaluation tool
- `generate_video_list.py` - Script to generate a list of videos with versioning
- `retrieve_videos_from_user_hash_id.py` - Tool to reproduce exact video pairs shown to a user
- `video_list.json` - Configuration file listing all available videos
- `videos/` - Directory containing video files for evaluation
- `AppsScript/` - Google Apps Script for data collection (if using Google Sheets)

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
