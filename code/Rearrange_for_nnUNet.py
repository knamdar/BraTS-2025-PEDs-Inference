#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 20:58:49 2025

@author: ernest
"""

import os
import shutil

# Define paths
input_root = "/data_skull_stripped"
output_root = "/data_skull_stripped_nnUNet"

# nnU-Net modality mapping
modality_map = {
    "t1n": "0000",
    "t1c": "0001",
    "t2f": "0002",
    "t2w": "0003"
}

# Ensure output directory exists
os.makedirs(output_root, exist_ok=True)

# Get list of patient directories
patient_dirs = sorted([
    d for d in os.listdir(input_root)
    if os.path.isdir(os.path.join(input_root, d))
])

if not patient_dirs:
    print("❌ No patient directories found in:", input_root)
    exit(1)

# Process each patient
for patient_id in patient_dirs:
    src_dir = os.path.join(input_root, patient_id)

    print(f"📦 Processing {patient_id}...")

    for modality, suffix in modality_map.items():
        src_file = os.path.join(src_dir, f"{patient_id}-{modality}.nii.gz")
        dst_file = os.path.join(output_root, f"{patient_id}_{suffix}.nii.gz")

        if os.path.exists(src_file):
            shutil.copy(src_file, dst_file)
            print(f"  ✅ {modality} → {dst_file}")
        else:
            print(f"  ⚠️  Missing {modality} for {patient_id}")

print("\n✅ Rearrangement complete.")
print(f"📂 All output saved to: {output_root}")
