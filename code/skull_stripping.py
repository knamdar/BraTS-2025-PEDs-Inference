#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply skull stripping using SynthStrip (FreeSurfer) to T1N images
from nested patient subfolders. Mask all four modalities.

Ernest Namdar
"""

import os
import sys
import nibabel as nib
import numpy as np
import subprocess

# === Docker-Mounted Paths ===
input_root = "/input"
output_root = "/data_skull_stripped"
mask_dir = "/brain_masks"
freesurfer_synthstrip = "/opt/freesurfer/bin/mri_synthstrip"
freesurfer_setup_script = "/opt/freesurfer/SetUpFreeSurfer.sh"

# === Ensure Output Folders Exist ===
os.makedirs(output_root, exist_ok=True)
os.makedirs(mask_dir, exist_ok=True)

# === Detect Patient Subdirectories ===
try:
    patient_dirs = sorted([
        d for d in os.listdir(input_root)
        if os.path.isdir(os.path.join(input_root, d))
    ])
except FileNotFoundError:
    print(f"❌ Input folder not found: {input_root}")
    sys.exit(1)

if not patient_dirs:
    print(f"❌ No subdirectories found in: {input_root}")
    sys.exit(1)

# === Modality Suffixes to Process ===
modalities = ["t1n", "t1c", "t2f", "t2w"]

# === Main Processing Loop ===
for pid in patient_dirs:
    input_dir = os.path.join(input_root, pid)
    output_dir = os.path.join(output_root, pid)
    os.makedirs(output_dir, exist_ok=True)

    t1n_file = os.path.join(input_dir, f"{pid}-t1n.nii.gz")
    brain_file = os.path.join(output_dir, f"{pid}-t1n.nii.gz")
    mask_file = os.path.join(mask_dir, f"{pid}_mask.nii.gz")
    temp_brain = brain_file.replace(".nii.gz", "_brain.nii.gz")

    if not os.path.exists(t1n_file):
        print(f"⚠️ Missing T1N: {t1n_file}, skipping {pid}")
        continue

    if os.path.exists(mask_file):
        print(f"✅ Mask already exists for {pid}, skipping SynthStrip.")
    else:
        print(f"🧠 Running SynthStrip on {pid}...")
        cmd = f"""
        export FREESURFER_HOME=/opt/freesurfer && \
        source {freesurfer_setup_script} && \
        {freesurfer_synthstrip} --i "{t1n_file}" --o "{temp_brain}" --mask "{mask_file}"
        """
        try:
            subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
            os.rename(temp_brain, brain_file)
        except subprocess.CalledProcessError as e:
            print(f"❌ SynthStrip failed for {pid}: {e}")
            continue

    # Apply the mask to all modalities
    try:
        mask_data = nib.load(mask_file).get_fdata()
    except Exception as e:
        print(f"❌ Failed to load mask for {pid}: {e}")
        continue

    for modality in modalities:
        in_file = os.path.join(input_dir, f"{pid}-{modality}.nii.gz")
        if not os.path.exists(in_file):
            print(f"⚠️ Missing modality: {in_file}")
            continue
        try:
            img = nib.load(in_file)
            masked_data = img.get_fdata() * mask_data
            masked_img = nib.Nifti1Image(masked_data, img.affine, img.header)
            out_file = os.path.join(output_dir, f"{pid}-{modality}.nii.gz")
            nib.save(masked_img, out_file)
            print(f"✅ Saved masked: {out_file}")
        except Exception as e:
            print(f"❌ Failed to process {in_file}: {e}")

print("\n🎯 Skull stripping completed for all cases.")
print(f"📂 Output images saved to: {output_root}")
print(f"📂 Brain masks saved to:   {mask_dir}")
