#!/bin/bash

echo "🚀 Starting full pipeline..."

# Step 1: Skull Stripping
echo "🔪 Step 1: Running skull_stripping.py"
python /code/skull_stripping.py || { echo "❌ Failed at skull_stripping.py"; exit 1; }

# Step 2: Rearranging for nnUNet
echo "📦 Step 2: Running Rearrange_for_nnUNet.py"
python /code/Rearrange_for_nnUNet.py || { echo "❌ Failed at Rearrange_for_nnUNet.py"; exit 1; }

# Step 3: Whole Tumor Inference
echo "🧠 Step 3: Running InferenceWT.sh"
bash /code/InferenceWT.sh || { echo "❌ Failed at InferenceWT.sh"; exit 1; }

# Step 4: Cropping Output Images
echo "✂️  Step 4: Running Cropping_Ts.py"
python /code/Cropping_Ts.py || { echo "❌ Failed at Cropping_Ts.py"; exit 1; }

# Step 5: Label 1 Inference
echo "🔍 Step 5: Running InferenceLb1.sh"
bash /code/InferenceLb1.sh || { echo "❌ Failed at InferenceLb1.sh"; exit 1; }

# Step 6: Label 2 Inference
echo "🔍 Step 6: Running InferenceLb2.sh"
bash /code/InferenceLb2.sh || { echo "❌ Failed at InferenceLb2.sh"; exit 1; }

# Step 7: Label 3 Inference
echo "🔍 Step 7: Running InferenceLb3.sh"
bash /code/InferenceLb3.sh || { echo "❌ Failed at InferenceLb3.sh"; exit 1; }

# Step 8: Label 4 Inference
echo "🔍 Step 8: Running InferenceLb4.sh"
bash /code/InferenceLb4.sh || { echo "❌ Failed at InferenceLb4.sh"; exit 1; }

# Step 9: Fusion
echo "🧬 Step 9: Running fusion_v2.py"
python /code/fusion_v2.py || { echo "❌ Failed at fusion_v2.py"; exit 1; }

# Step 10: Clean Up
echo "🧹 Step 10: Running flush_temp_folders.py"
python /code/flush_temp_folders.py || { echo "❌ Failed at flush_temp_folders.py"; exit 1; }

echo "✅ Pipeline completed successfully!"

