import os
import json
import sys
import time
import hashlib
from datetime import datetime
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

def calculate_files_hash(file_list):
    """Calculate a hash of the file list for versioning purposes."""
    # Create a string with all filenames and their last modified times
    content = ''
    for file_path in file_list:
        try:
            mtime = os.path.getmtime(file_path)
            size = os.path.getsize(file_path)
            content += f"{file_path}:{mtime}:{size}\n"
        except Exception:
            # If file doesn't exist, just use the path
            content += f"{file_path}\n"
    
    # Generate SHA-256 hash
    hash_obj = hashlib.sha256(content.encode())
    return hash_obj.hexdigest()[:16]  # First 16 chars of hash is enough

def generate_video_list(directory):
    """Generate the video list in the format needed for the frontend."""
    video_files = get_video_files(directory)
    
    # Sort files alphabetically for consistency
    video_files.sort()
    
    # Generate version information
    timestamp = datetime.now().isoformat()
    version = f"1.0.{int(time.time())}"  # Simple versioning scheme
    files_hash = calculate_files_hash(video_files)
    
    # Create the full structure
    result = {
        "version": version,
        "generated_at": timestamp,
        "hash": files_hash,
        "files": video_files
    }
    
    return result

def main():
    # Directory containing the video files
    video_dir = 'videos'
    
    try:
        # Check if videos directory exists
        if not os.path.exists(video_dir):
            print(f"Error: Directory '{video_dir}' does not exist", file=sys.stderr)
            sys.exit(1)
            
        # Generate the video list with version info
        video_list_data = generate_video_list(video_dir)
        
        # Save to file
        with open('video_list.json', 'w') as f:
            json.dump(video_list_data, f, indent=2)
        
        # Create a timestamped backup copy
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f'video_list_{timestamp}.json'
        with open(backup_filename, 'w') as f:
            json.dump(video_list_data, f, indent=2)
            
        # Print summary
        print(f"Generated video list with {len(video_list_data['files'])} videos")
        print(f"Version: {video_list_data['version']}")
        print(f"Hash: {video_list_data['hash']}")
        print(f"Backup saved to: {backup_filename}")
        print("\nIMPORTANT: Keep this version information for future reproducibility!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 