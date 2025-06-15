#!/usr/bin/env python3
"""
Sample Data Generator for QoE Analysis

This script generates a sample CSV file with synthetic QoE assessment data
that can be used to test the analysis script without needing to download
data from the Google Sheet.
"""

import os
import csv
import random
import datetime

# Constants
OUTPUT_FILE = "sample_qoe_data.csv"
NUM_USERS = 20
NUM_EVALUATIONS_PER_USER = 5

# Sample video files
REAL_VIDEOS = [
    "videos/original_video.mp4",
    "videos/original_video_1280_720.mp4",
    "videos/original_video_upsampled_from_1280_720_to_1920_1080.mp4"
]

SYNTHETIC_VIDEOS = [
    "videos/interpolated_rife_1280_720_30fps.mp4",
    "videos/interpolated_video_addWeighted.mp4",
    "videos/interpolated_video_film.mp4",
    "videos/video_with_degrad_mk11_1080p.mp4"
]

# Possible responses
REAL_VIDEO_OPTIONS = ["a", "b", "both", "none"]
GAMEPLAY_AFFECTED_OPTIONS = ["yes", "no", "maybe", "not-applicable"]
INFORM_PREFERENCE_OPTIONS = ["yes", "no", "does-not-matter"]
VISUAL_CUES_OPTIONS = [
    "lighting", "animation", "background", "movement", 
    "textures", "artifacts", "none"
]

def generate_user_id(length=10):
    """Generate a random user ID."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_timestamp():
    """Generate a random timestamp within the last month."""
    now = datetime.datetime.now()
    days_ago = random.randint(0, 30)
    minutes_ago = random.randint(0, 1440)
    dt = now - datetime.timedelta(days=days_ago, minutes=minutes_ago)
    return dt.isoformat()

def generate_sample_data():
    """Generate sample QoE assessment data."""
    data = []
    
    # Add header row
    header = [
        "Timestamp", "User ID", "Scene", 
        "Video A Filename", "Video B Filename",
        "Video A Score", "Video B Score",
        "Video A Comment", "Video B Comment",
        "Video A Is Real", "Video B Is Real",
        "Which Video Real", "Gameplay Affected",
        "Inform Preference", "Visual Cues",
        "Other Cues", "Video List Version",
        "Video List Hash", "Video List Timestamp"
    ]
    data.append(header)
    
    # Generate data for each user
    for _ in range(NUM_USERS):
        user_id = generate_user_id()
        
        for i in range(NUM_EVALUATIONS_PER_USER):
            # Randomly select videos
            video_a = random.choice(REAL_VIDEOS + SYNTHETIC_VIDEOS)
            # Make sure video B is different from video A
            video_b = random.choice([v for v in (REAL_VIDEOS + SYNTHETIC_VIDEOS) if v != video_a])
            
            # Determine if videos are real or synthetic
            video_a_is_real = "TRUE" if video_a in REAL_VIDEOS else "FALSE"
            video_b_is_real = "TRUE" if video_b in REAL_VIDEOS else "FALSE"
            
            # Generate random scores (slightly higher for real videos to simulate user preference)
            video_a_score = random.randint(1, 5)
            if video_a in REAL_VIDEOS:
                video_a_score = min(5, video_a_score + random.randint(0, 1))
                
            video_b_score = random.randint(1, 5)
            if video_b in REAL_VIDEOS:
                video_b_score = min(5, video_b_score + random.randint(0, 1))
            
            # Generate user's guess about which video is real
            # Make it somewhat accurate (70% chance of being correct)
            if random.random() < 0.7:
                # Correct guess
                if video_a_is_real == "TRUE" and video_b_is_real == "TRUE":
                    which_video_real = "both"
                elif video_a_is_real == "FALSE" and video_b_is_real == "FALSE":
                    which_video_real = "none"
                elif video_a_is_real == "TRUE" and video_b_is_real == "FALSE":
                    which_video_real = "a"
                else:  # video_a_is_real == "FALSE" and video_b_is_real == "TRUE"
                    which_video_real = "b"
            else:
                # Incorrect guess (random)
                which_video_real = random.choice(REAL_VIDEO_OPTIONS)
            
            # Generate other responses
            gameplay_affected = random.choice(GAMEPLAY_AFFECTED_OPTIONS)
            inform_preference = random.choice(INFORM_PREFERENCE_OPTIONS)
            
            # Generate visual cues (1-3 random cues)
            num_cues = random.randint(1, 3)
            visual_cues = ",".join(random.sample(VISUAL_CUES_OPTIONS, num_cues))
            
            # Create row
            row = [
                generate_timestamp(),
                user_id,
                f"Pair {i+1}",
                video_a,
                video_b,
                str(video_a_score),
                str(video_b_score),
                "N/A",  # Video A Comment
                "N/A",  # Video B Comment
                video_a_is_real,
                video_b_is_real,
                which_video_real,
                gameplay_affected,
                inform_preference,
                visual_cues,
                "N/A",  # Other Cues
                "1.0.1748023680",  # Video List Version
                "4d8c354974be9f7c",  # Video List Hash
                "2025-05-23T18:08:00.109046+00:00"  # Video List Timestamp
            ]
            data.append(row)
    
    return data

def save_to_csv(data, filename):
    """Save data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"Sample data saved to {filename}")
    print(f"Generated {len(data) - 1} sample evaluations for {NUM_USERS} users")

def main():
    """Main function."""
    print("Generating sample QoE assessment data...")
    data = generate_sample_data()
    save_to_csv(data, OUTPUT_FILE)
    
    print("\nNext steps:")
    print(f"1. Run the analysis script: python analyze_qoe_data.py --csv {OUTPUT_FILE}")
    print("2. Check the 'visualizations' directory for the generated graphs")

if __name__ == "__main__":
    main()
