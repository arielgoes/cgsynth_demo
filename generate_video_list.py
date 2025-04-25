import os
import re
import json
import sys
from pathlib import Path

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
        else:
            print(f"Warning: Scene {scene} is missing either real or interpolated video", file=sys.stderr)
    
    return video_list

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
        print(f"Generated video list with {len(video_list)//2} scenes and {len(video_list)} videos")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 