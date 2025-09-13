#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 00:33:42 2025

@author: ernest
"""

import os
import nibabel as nib
import numpy as np
import pandas as pd
from glob import glob

# --- Config ---
input_image_dir = "/data_skull_stripped_nnUNet"
input_label_dir = "/PredictedWholeTumoreMasks"
output_image_dir = "/Dataset007_BraTS2025_PedCropped/imagesTs"
output_label_dir = "/Dataset007_BraTS2025_PedCropped/labelsTs_WT"
csv_log_path = "/crop_coordinates_Ts.csv"

margin = 8        # voxels
min_size = 48     # cube minimum edge length
num_channels = 4  # number of image modalities

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

crop_log = []

def make_cube_bbox(bbox_min, bbox_max, shape, margin, min_size):
    bbox_min = np.maximum(0, bbox_min - margin)
    bbox_max = np.minimum(shape, bbox_max + margin)

    size = bbox_max - bbox_min
    max_len = max(np.max(size), min_size)

    center = (bbox_min + bbox_max) // 2
    half_len = max_len // 2

    new_min = np.maximum(0, center - half_len)
    new_max = np.minimum(shape, new_min + max_len)

    new_min = new_max - max_len  # ensure exact size
    return new_min, new_max

# --- Process each case ---
for label_path in sorted(glob(os.path.join(input_label_dir, "*.nii.gz"))):
    case_id = os.path.basename(label_path).replace(".nii.gz", "")
    label_nii = nib.load(label_path)
    label_data = label_nii.get_fdata()

    mask = label_data > 0
    if not np.any(mask):
        print(f"⚠️ No tumor found in {case_id}, skipping.")
        continue

    coords = np.array(np.where(mask))
    bbox_min = coords.min(axis=1)
    bbox_max = coords.max(axis=1) + 1

    crop_min, crop_max = make_cube_bbox(bbox_min, bbox_max, label_data.shape, margin, min_size)

    cropped_label = label_data[
        crop_min[0]:crop_max[0],
        crop_min[1]:crop_max[1],
        crop_min[2]:crop_max[2]
    ]
    cropped_label_nii = nib.Nifti1Image(cropped_label.astype(np.uint8), label_nii.affine, label_nii.header)
    nib.save(cropped_label_nii, os.path.join(output_label_dir, f"{case_id}.nii.gz"))

    for ch in range(num_channels):
        img_path = os.path.join(input_image_dir, f"{case_id}_{ch:04d}.nii.gz")
        img_nii = nib.load(img_path)
        img_data = img_nii.get_fdata()
        cropped_img = img_data[
            crop_min[0]:crop_max[0],
            crop_min[1]:crop_max[1],
            crop_min[2]:crop_max[2]
        ]
        cropped_img_nii = nib.Nifti1Image(cropped_img.astype(np.float32), img_nii.affine, img_nii.header)
        nib.save(cropped_img_nii, os.path.join(output_image_dir, f"{case_id}_{ch:04d}.nii.gz"))

    crop_log.append({
        "case_id": case_id,
        "x_min": int(crop_min[0]), "x_max": int(crop_max[0]),
        "y_min": int(crop_min[1]), "y_max": int(crop_max[1]),
        "z_min": int(crop_min[2]), "z_max": int(crop_max[2]),
        "crop_size": f"{crop_max[0]-crop_min[0]}x{crop_max[1]-crop_min[1]}x{crop_max[2]-crop_min[2]}"
    })

    print(f"✅ Cropped {case_id}: {crop_log[-1]['crop_size']}")

# Save crop coordinates to CSV
df_log = pd.DataFrame(crop_log)
df_log.to_csv(csv_log_path, index=False)
print(f"\n📝 Saved crop log to: {csv_log_path}")
