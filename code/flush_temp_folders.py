#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 19:17:55 2025

@author: ernest
"""

import shutil
import os

# Paths to delete (directories)
dirs_to_delete = [
    "/data_skull_stripped",
    "/brain_masks",
    "/data_skull_stripped_nnUNet",
    "/PredictedWholeTumoreMasks",
    "/Dataset007_BraTS2025_PedCropped",
    "/PredictedLb1Masks",
    "/PredictedLb2Masks",
    "/PredictedLb3Masks",
    "/PredictedLb4Masks"
]

# File to delete
file_to_delete = "/crop_coordinates_Ts.csv"

# Delete directories
for path in dirs_to_delete:
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"🗑️ Deleted directory: {path}")
        except Exception as e:
            print(f"❌ Failed to delete {path}: {e}")
    else:
        print(f"ℹ️ Directory does not exist: {path}")

# Delete file
if os.path.exists(file_to_delete):
    try:
        os.remove(file_to_delete)
        print(f"🗑️ Deleted file: {file_to_delete}")
    except Exception as e:
        print(f"❌ Failed to delete file {file_to_delete}: {e}")
else:
    print(f"ℹ️ File does not exist: {file_to_delete}")

