import scipy.io as sio
import pandas as pd
import numpy as np
import os
from datetime import datetime

def check_raw_alignment(subject_folder, night="1"):
    hr_path = os.path.join(subject_folder, night, "hr.csv")
    mat_path = os.path.join(subject_folder, night, "labels.mat")
    
    # 1. Inspect .mat file structure
    mat_contents = sio.loadmat(mat_path)
    rec_start_str = mat_contents['recStart'][0]
    if isinstance(rec_start_str, np.ndarray): rec_start_str = rec_start_str[0]
    
    print(f"=== 🕒 TIMING DIAGNOSTIC: NIGHT {night} ===")
    print(f"MAT recStart string        : {rec_start_str.strip()}")
    
    rec_start_ts = datetime.strptime(rec_start_str.strip(), "%Y-%m-%d %H:%M:%S").timestamp()
    print(f"MAT recStart Unix Epoch    : {rec_start_ts}")
    
    # 2. Inspect hr.csv timestamps
    hr_df = pd.read_csv(hr_path, header=None, names=['timestamp', 'hr'])
    first_hr_ts = hr_df['timestamp'].iloc[0]
    last_hr_ts = hr_df['timestamp'].iloc[-1]
    
    print(f"CSV First Heart Rate Epoch : {first_hr_ts} -> ({datetime.fromtimestamp(first_hr_ts)})")
    print(f"CSV Last Heart Rate Epoch  : {last_hr_ts} -> ({datetime.fromtimestamp(last_hr_ts)})")
    
    # 3. Check Delta Mismatch
    time_delta_hours = (first_hr_ts - rec_start_ts) / 3600
    print(f"Calculated Time Mismatch   : {time_delta_hours:.2f} hours")
    
    # 4. Check First 20 Raw Labels vs Last 20 Raw Labels
    stages = mat_contents['expert_label'].flatten()
    print(f"\nFirst 30 raw stages in MAT array: {stages[:30].tolist()}")
    print(f"Last 30 raw stages in MAT array : {stages[-30:].tolist()}")

check_raw_alignment("./data/00", night="1")