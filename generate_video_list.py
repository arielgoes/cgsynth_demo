import os
import json
import sys
from pathlib import Path

def get_video_files(directory):
    """Get all video files from the directory and its subdirectories."""
    video_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp4'):
                # Convert path to use forward slashes for web compatibility
                relative_path = os.path.join(root, file).replace('\\', '/')
                video_files.append(relative_path)
    
    return video_files

def generate_video_list(directory):
    """Generate the video list in the format needed for the frontend."""
    video_files = get_video_files(directory)
    
    # Sort files alphabetically for consistency
    video_files.sort()
    
    return video_files

def main():
    # Directory containing the video files
    video_dir = 'videos'
    
    try:
        # Check if videos directory exists
        if not os.path.exists(video_dir):
            print(f"Error: Directory '{video_dir}' does not exist", file=sys.stderr)
            sys.exit(1)
            
        # Generate the video list
        video_list = generate_video_list(video_dir)
        
        # Save to file
        with open('video_list.json', 'w') as f:
            json.dump(video_list, f, indent=2)
            
        # Print summary
        print(f"Generated video list with {len(video_list)} videos")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 