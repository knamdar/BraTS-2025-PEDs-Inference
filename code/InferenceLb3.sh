#!/bin/bash

# Set nnU-Net environment paths
export nnUNet_raw="/nnUNet_raw"
export nnUNet_preprocessed="/nnUNet_preprocessed"
export nnUNet_results="/nnUNet_results"

# Prediction settings
DATASET_ID=009
CONFIG="3d_fullres"
INPUT_DIR="/Dataset007_BraTS2025_PedCropped/imagesTs"
OUTPUT_DIR="/PredictedLb3Masks"

echo "🔁 Running prediction for Dataset ${DATASET_ID} using $CONFIG..."
echo "📂 Input: $INPUT_DIR"
echo "📁 Output: $OUTPUT_DIR"

# Run prediction on the whole batch
nnUNetv2_predict \
    -d ${DATASET_ID} \
    -c ${CONFIG} \
    -f all \
    -i "${INPUT_DIR}" \
    -o "${OUTPUT_DIR}"

echo "✅ All predictions completed!"

