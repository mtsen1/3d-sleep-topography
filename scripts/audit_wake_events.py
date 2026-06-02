import scipy.io as sio
import os
import numpy as np

def audit_wake_fragmentation(subject_folder, target_night="1"):
    mat_path = os.path.join(subject_folder, target_night, "labels.mat")
    
    if not os.path.exists(mat_path):
        print("Target night folder missing.")
        return
        
    mat_contents = sio.loadmat(mat_path)
    expert_labels = mat_contents['expert_label'].flatten()
    
    # Filter out unscored blocks (5)
    valid_labels = expert_labels[expert_labels != 5]
    
    # 0 = Wake, 1 = N1, 2 = N2, 3 = N3, 4 = REM
    wake_epochs = (valid_labels == 0).astype(int)
    total_wake_mins = (np.sum(wake_epochs) * 30) / 60
    total_sleep_mins = (len(valid_labels) * 30) / 60
    
    # Calculate distinct awakening episodes
    # Finding transitions where the previous epoch wasn't wake, but the current one is
    wake_transitions = np.diff(np.insert(wake_epochs, 0, 0))
    num_awakenings = np.sum(wake_transitions == 1)
    
    print(f"=== 🔍 WAKE FRAGMENTATION AUDIT: NIGHT {target_night} ===")
    print(f"Total Recording Time : {total_sleep_mins:.1f} minutes")
    print(f"Total Time Awake     : {total_wake_mins:.1f} minutes")
    print(f"Wake Percentage      : {(total_wake_mins / total_sleep_mins)*100:.1f}%")
    print(f"Number of Awakenings : {num_awakenings} distinct events")
    
    # Let's look at the distribution of awakening lengths
    if num_awakenings > 0:
        wake_runs = []
        current_run = 0
        for epoch in wake_epochs:
            if epoch == 1:
                current_run += 1
            elif current_run > 0:
                wake_runs.append(current_run * 30 / 60) # convert to minutes
                current_run = 0
        if current_run > 0:
            wake_runs.append(current_run * 30 / 60)
            
        print(f"Shortest Awakening   : {min(wake_runs):.2f} mins")
        print(f"Longest Awakening    : {max(wake_runs):.2f} mins")
        print(f"Average Wake Event   : {np.mean(wake_runs):.2f} mins")

audit_wake_fragmentation("./data/07", target_night="1")