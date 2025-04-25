import os
import re
import json
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VideoHandler(FileSystemEventHandler):
    def __init__(self, video_dir):
        self.video_dir = video_dir
        self.last_update = 0
        self.update_delay = 1  # seconds

    def on_any_event(self, event):
        # Only process if it's a video file
        if not event.is_directory and Path(event.src_path).suffix.lower() in {'.mp4', '.webm', '.mov', '.avi'}:
            current_time = time.time()
            # Debounce updates to prevent multiple rapid updates
            if current_time - self.last_update >= self.update_delay:
                self.last_update = current_time
                print(f"\nDetected change in video files: {event.event_type} - {event.src_path}")
                generate_and_save_video_list(self.video_dir)

def get_video_files(directory):
    """Get all video files from the directory and its subdirectories."""
    video_extensions = {'.mp4', '.webm', '.mov', '.avi'}
    video_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in video_extensions:
                # Convert path to use forward slashes for web compatibility
                relative_path = os.path.join(root, file).replace('\\', '/')
                video_files.append(relative_path)
    
    return video_files

def group_videos_by_scene(video_files):
    """Group video files by scene name."""
    scene_groups = {}
    
    for file in video_files:
        # Extract scene name using regex (e.g., "scene_01" from "videos/scene_01_real.mp4")
        match = re.search(r'scene_\d+', file)
        if match:
            scene_name = match.group(0)
            if scene_name not in scene_groups:
                scene_groups[scene_name] = []
            scene_groups[scene_name].append(file)
    
    return scene_groups

def generate_video_list(directory):
    """Generate the video list in the format needed for the frontend."""
    video_files = get_video_files(directory)
    scene_groups = group_videos_by_scene(video_files)
    
    # Sort scenes numerically
    sorted_scenes = sorted(scene_groups.keys(), 
                         key=lambda x: int(re.search(r'\d+', x).group()))
    
    # Generate the list in the format needed for the frontend
    video_list = []
    for scene in sorted_scenes:
        files = scene_groups[scene]
        real_file = next((f for f in files if '_real' in f), None)
        interp_file = next((f for f in files if '_interp' in f), None)
        
        if real_file and interp_file:
            video_list.extend([real_file, interp_file])
    
    return video_list

def generate_and_save_video_list(directory):
    """Generate and save the video list to a JSON file."""
    try:
        video_list = generate_video_list(directory)
        
        # Print the list to console
        print("\nCurrent video list:")
        print(json.dumps(video_list, indent=2))
        
        # Save to file
        with open('video_list.json', 'w') as f:
            json.dump(video_list, f, indent=2)
        print("\nVideo list saved to video_list.json")
        
        # Print summary
        print(f"\nTotal scenes: {len(video_list)//2}")
        print(f"Total videos: {len(video_list)}")
        
    except Exception as e:
        print(f"Error generating video list: {e}")

def main():
    # Directory containing the video files
    video_dir = 'videos'  # Change this to your video directory
    
    # Create the directory if it doesn't exist
    os.makedirs(video_dir, exist_ok=True)
    
    # Initial generation of video list
    print("Initial video list generation...")
    generate_and_save_video_list(video_dir)
    
    # Set up the file system observer
    event_handler = VideoHandler(video_dir)
    observer = Observer()
    observer.schedule(event_handler, video_dir, recursive=True)
    observer.start()
    
    print(f"\nWatching directory '{video_dir}' for changes...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching directory")
    
    observer.join()

if __name__ == "__main__":
    main() 