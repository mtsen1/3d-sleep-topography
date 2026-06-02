import pandas as pd
import numpy as np
import scipy.io as sio
import scipy.ndimage as ndimage
import json
import os
from datetime import datetime

def process_subject_perfect_terrain(subject_folder, total_grid_steps=240):
    night_subdirs = [d for d in os.listdir(subject_folder) if os.path.isdir(os.path.join(subject_folder, d)) and d.isdigit()]
    night_subdirs = sorted(night_subdirs, key=int)
    
    raw_matrix = []
    # 0 = Wake, 1 = N1, 2 = N2, 3 = N3, 4 = REM
    stage_altitude_map = {0: 18.0, 1: 12.0, 2: 8.0, 4: 10.0, 3: 1.5}
    
    for night in night_subdirs:
        hr_path = os.path.join(subject_folder, night, "hr.csv")
        mat_path = os.path.join(subject_folder, night, "labels.mat")
        
        if not (os.path.exists(hr_path) and os.path.exists(mat_path)):
            continue
            
        # --- Metadata Parsing ---
        mat_contents = sio.loadmat(mat_path)
        rec_start_str = mat_contents['recStart'][0]
        if isinstance(rec_start_str, np.ndarray): rec_start_str = rec_start_str[0]
        rec_start_ts = datetime.strptime(rec_start_str.strip(), "%Y-%m-%d %H:%M:%S").timestamp()
        stages = mat_contents['expert_label'].flatten()
        
        # --- Data Cleansing & Alignment Pass ---
        hr_df = pd.read_csv(hr_path, header=None, names=['timestamp', 'hr'])
        
        # 💡 FIXED TIME-ZONE ALIGNMENT MATH:
        # Calculate exactly which 30-second epoch of the sleep study each heart rate row lands on.
        # This preserves the true mapping coordinates even if the CSV file started hours early.
        hr_df['epoch_idx'] = np.floor((hr_df['timestamp'] - rec_start_ts) / 30).astype(int)
        
        # Keep ONLY rows where the heart rate timestamp falls inside the active window of the sleep study
        hr_df = hr_df[(hr_df['epoch_idx'] >= 0) & (hr_df['epoch_idx'] < len(stages))]
        
        if len(hr_df) == 0:
            print(f"Warning: Zero overlapping epochs found on Night {night}. Skipping.")
            continue
            
        # Map the true sleep stages to our filtered timestamps
        hr_df['stage'] = hr_df['epoch_idx'].map(lambda idx: stages[idx])
        
        # Strip out un-scored artifact epochs (5)
        hr_df = hr_df[hr_df['stage'] != 5]
        
        if len(hr_df) == 0:
            continue
            
        # 💡 CONVERT TO PURE NUMERIC ARRAY BEFORE SPLITTING
        # Map stages directly to altitudes for the whole night at once
        full_night_altitudes = hr_df['stage'].map(stage_altitude_map).fillna(8.0).values
        
        # 💡 MAJORITY-VOTE (MODE) TIME BUCKET RE-SAMPLER
        # Splitting the raw 1D numeric array into 240 equal sequential time buckets
        chunks = np.array_split(full_night_altitudes, total_grid_steps)
        
        night_heights = []
        for chunk in chunks:
            if len(chunk) > 0:
                # 🌟 Count the frequencies of each height value inside this specific time bucket
                values, counts = np.unique(chunk, return_counts=True)
                
                # Find the value that appears most frequent (the statistical mode)
                majority_height = values[np.argmax(counts)]
                night_heights.append(float(majority_height))
            else:
                night_heights.append(8.0)
                
        raw_matrix.append(night_heights)
        
    height_grid = np.array(raw_matrix, dtype=float)
    
    # Return the pure, un-blurred raw majority-vote data matrix to let frontend step-functions control formatting
    return height_grid.tolist()

# Target data path cohort setup
subject_dir = "./data/00" 

if not os.path.exists("./public"):
    os.makedirs("./public")

print("Processing subject matrix telemetry...")
heightmap_data = process_subject_perfect_terrain(subject_dir)

with open("./public/sleep_terrain.json", "w") as f:
    json.dump({"heightmap": heightmap_data}, f)

print(f"Perfect calibration matrix compiled successfully across {len(heightmap_data)} nights!")