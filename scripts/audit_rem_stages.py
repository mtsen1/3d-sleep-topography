import scipy.io as sio
import os
import numpy as np

def audit_subject_rem(subject_folder):
    night_subdirs = [d for d in os.listdir(subject_folder) if os.path.isdir(os.path.join(subject_folder, d)) and d.isdigit()]
    night_subdirs = sorted(night_subdirs, key=int)
    
    print(f"=== 📊 SLEEP AUDIT FOR SUBJECT: {os.path.basename(subject_folder)} ===")
    
    for night in night_subdirs:
        mat_path = os.path.join(subject_folder, night, "labels.mat")
        if not os.path.exists(mat_path):
            continue
            
        mat_contents = sio.loadmat(mat_path)
        # 0 = Wake, 1 = N1, 2 = N2, 3 = N3, 4 = REM
        expert_labels = mat_contents['expert_label'].flatten()
        
        # Strip out un-scored artifact epochs (5)
        valid_labels = expert_labels[expert_labels != 5]
        
        # Calculate real duration metrics (each epoch = 30 seconds)
        total_epochs = len(valid_labels)
        rem_epochs = np.sum(valid_labels == 4)
        
        total_minutes = (total_epochs * 30) / 60
        rem_minutes = (rem_epochs * 30) / 60
        rem_percentage = (rem_epochs / total_epochs) * 100 if total_epochs > 0 else 0
        
        print(f"Night {night}: Total Sleep: {total_minutes:.1f} mins | Actual REM: {rem_minutes:.1f} mins ({rem_percentage:.1f}%)")

# Execute audit on Bidslab00
audit_subject_rem("./data/00")