#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 07:21:05 2025

@author: ernest
"""

import os
import nibabel as nib
import numpy as np
import pandas as pd
from glob import glob

# Prediction folders (in ET, NET, CC, ED order)
pred_dirs = [
    "/PredictedLb1Masks",         # ET
    "/PredictedLb2Masks",    # NET
    "/PredictedLb3Masks",    # CC
    "/PredictedLb4Masks",    # ED
]

# Corresponding label values
label_values = [1, 2, 3, 4]

# Output path
output_dir = "/output"
os.makedirs(output_dir, exist_ok=True)

# Load crop coordinates
coords_df = pd.read_csv("/crop_coordinates_Ts.csv")
coords_df.set_index("case_id", inplace=True)

# Reference image path (with correct orientation and metadata)
ref_dir = "/PredictedWholeTumoreMasks"

# Process each case
for case_id in coords_df.index:
    ref_path = os.path.join(ref_dir, f"{case_id}.nii.gz")
    if not os.path.exists(ref_path):
        print(f"⚠️ Missing reference file: {ref_path}")
        continue

    # Load reference image to get shape, affine, and header
    ref_nii = nib.load(ref_path)
    ref_data = np.zeros(ref_nii.shape, dtype=np.uint8)
    affine = ref_nii.affine
    header = ref_nii.header

    # Get crop coordinates
    x_min, x_max = coords_df.loc[case_id, ['x_min', 'x_max']]
    y_min, y_max = coords_df.loc[case_id, ['y_min', 'y_max']]
    z_min, z_max = coords_df.loc[case_id, ['z_min', 'z_max']]

    # Fill in predictions
    for pred_dir, label_val in zip(pred_dirs, label_values):
        pred_path = os.path.join(pred_dir, f"{case_id}.nii.gz")
        if not os.path.exists(pred_path):
            print(f"⚠️ Missing prediction: {pred_path}")
            continue

        cropped = nib.load(pred_path).get_fdata().astype(np.uint8)
        expected_shape = (x_max - x_min, y_max - y_min, z_max - z_min)
        if cropped.shape != expected_shape:
            print(f"❌ Shape mismatch for {case_id} [label={label_val}]: {cropped.shape} vs {expected_shape}")
            continue

        ref_data[x_min:x_max, y_min:y_max, z_min:z_max][cropped == 1] = label_val

    # Save the combined result
    out_path = os.path.join(output_dir, f"{case_id}.nii.gz")
    nib.save(nib.Nifti1Image(ref_data, affine, header), out_path)
    print(f"✅ Saved combined prediction: {case_id}.nii.gz")

print(f"\n🎯 All orientation-safe predictions saved to:\n{output_dir}")
