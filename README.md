# 🧠 BraTS-2025-PEDs Inference Pipeline

This repository contains the full inference pipeline developed for the **BraTS-PEDs 2025 Challenge** on pediatric brain tumor segmentation.  
It implements a robust, reproducible, and uncertainty-enabled nnU-Net–based workflow that performs **whole tumor detection**, **subregion segmentation**, and **voxel-wise uncertainty mapping** to support clinical review.

---

## 📖 Overview

- **Exploratory Data Analysis (EDA):** First characterization of the BraTS-PEDs 2025 dataset, revealing subregion imbalance, intensity variation, and disconnected tumor islands.
- **Baseline Benchmarks:** Established nnU-Net v2 benchmarks for whole tumor and subregion segmentation.
- **Preprocessing Modules:** Evaluated skull stripping, cascading, and atlas-based masking to focus training on relevant brain regions.
- **Uncertainty Quantification:** Introduced voxel-wise ensemble methods to identify high-uncertainty regions and support human-in-the-loop review.

> **Key finding:** Skull stripping and atlas-based masking improved segmentation performance with minimal computational cost, while synthetic-channel augmentation had limited effect. The region-focused ensemble achieved the strongest ET/NET performance and generated uncertainty maps useful for clinical interpretation.

---

## ⚡ Pipeline Steps

The pipeline can be run with a **single command** via `code/pipeline.sh`.  
It performs the following steps sequentially:

1. **Skull Stripping** → `skull_stripping.py`
2. **Rearrange for nnU-Net** → `Rearrange_for_nnUNet.py`
3. **Whole Tumor Inference** → `InferenceWT.sh`
4. **Crop Outputs Around Tumor** → `Cropping_Ts.py`
5. **Label 1 Inference** → `InferenceLb1.sh`
6. **Label 2 Inference** → `InferenceLb2.sh`
7. **Label 3 Inference** → `InferenceLb3.sh`
8. **Label 4 Inference** → `InferenceLb4.sh`
9. **Fusion of Subregions** → `fusion_v2.py`
10. **Clean Temporary Folders** → `flush_temp_folders.py`

Each step logs progress and stops gracefully if an error occurs.

---

## 🚀 Running Locally

### Requirements

- **Python 3.9+**
- [nnU-Net v2](https://github.com/MIC-DKFZ/nnUNet)
- FreeSurfer (mount your FreeSurfer directory beside code and data as freesurfer)

Run the pipeline:

```bash
bash code/pipeline.sh
```

Input and output folder paths should be configured in your environment before running.

---

## 🐳 Running with Docker

We also provide a pre-built Docker image for easy reproducibility.

### 1. One-Shot Run (automatically runs pipeline)

```bash
docker run --rm --gpus all   --shm-size=8g   -v /path/to/data:/input:ro   -v /path/to/output:/output   knamdar/bratsped25namdar /bin/bash
```

### 2. Interactive Session (stay inside container)

```bash
docker run -it --gpus all   --shm-size=8g   -v /path/to/data:/input:ro   -v /path/to/output:/output   knamdar/bratsped25namdar /bin/bash
```

Replace `/path/to/data` and `/path/to/output` with your actual input/output directories.

---

## 📂 Repository Structure

```
code/                # Pipeline scripts (main: pipeline.sh)
data/                # Input data (not tracked)
inference/           # Inference outputs
nnUNet/              # nnU-Net configs and results (with LFS-tracked checkpoints)
documents/           # Poster and related documentation
```

---

## 📜 Citation

If you use this repository, please cite our work:

> **Namdar, K., Mirjalili, S., Kim, S., Deniffel, D., Brunt, K., Celi, L.A., Cusimano, M., Tyrrell, P.N.**  
> *Enabling Uncertainty Measurement in Multi-Subregion Tumor Segmentation: BraTS 2025 Pediatrics.*  
> MICCAI 2025 Pediatric Brain Tumor Segmentation Challenge Poster.

---

## 📝 License

This repository is released under the MIT License. See [LICENSE](LICENSE) for details.
