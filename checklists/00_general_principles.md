# General Principles & Data Foundation

> **Scope:** Applies to ALL GeoAI tasks (Classification, Segmentation, Detection, Regression).
> **Goal:** Ensure data physical validity and prevent spatial leakage.

## 1. Spatial Integrity
*If the geography is wrong, the math doesn't matter.*

- [ ] **CRS Standardization:** Are all input rasters and vector labels projected to the same **Projected CRS** (e.g., UTM)?
    - *Avoid:* Mixing WGS84 (Lat/Lon) with Metric projections.
    - *Why:* To preserve accurate area/distance representation for convolutions.
    - *Tools:* `utils/check_data_integrity.py`
- [ ] **Pixel Alignment (Snapping):** Are pixels from different sensors (e.g., Sentinel-2 and Landsat) aligned to the exact same grid?
    - *Risk:* Sub-pixel misalignment (e.g., offset by 0.5 pixels) introduces significant noise at edges, confusing the model during fusion.
- [ ] **The "Tobler" Test (Spatial Splitting):** Is the Train/Val/Test split performed by **Geographic Blocks**, NOT by random shuffling of patches?
    - *Risk:* Random split = **Data Leakage**. Due to [Tobler's First Law](https://en.wikipedia.org/wiki/Tobler's_first_law_of_geography) ("near things are more related"), a random split places almost identical training samples into the test set, inflating accuracy artificially.
    - *Action:* Use Block Cross-Validation (e.g., Train on West region, Test on East region).
    - *Tools:* `utils/check_spatial_leakage.py`
- [ ] **Buffer Zones:** Is there a physical gap (buffer) between Training blocks and Test blocks?
    - *Context:* Deep Learning models have large receptive fields (effective context).
    - *Risk:* Without a buffer, edge pixels in the Test block "see" context from the Training block, causing leakage.

## 2. Data Hygiene & Labels
*Garbage In, Garbage Out.*

- [ ] **NoData Masking:** Are `NoData` / Padding values (e.g., `-9999`, `0`, `NaN`) explicitly masked out in the Loss function?
    - *Risk:* The model learns that "black rectangular borders" (padding) are a specific class, or gradients explode due to extreme values like `-9999`.
    - *Action:* Set a `ignore_index` in CrossEntropyLoss, or use a boolean mask in custom losses.
    - *Tools:* `utils/check_data_integrity.py` (Reports missing NoData values)
- [ ] **Temporal Consistency:** Do the training images and ground truth labels match chronologically?
    - *Risk:* Using 2023 imagery with 2015 labels is only valid for change detection, not classification.
    - *Action:* Filter data by date or use stable land-cover classes.

## 3. Preprocessing Leakage
*Preventing statistical leakage.*

- [ ] **Normalization Stats:** Are Mean/Std calculated **only on the Training Set**?
    - *Risk:* Calculating global Mean/Std across the whole dataset leaks information about the Test set distribution to the model during training.
    - *Action:* Compute stats on Train split, save them, and apply (`transform`) to Val/Test splits.
- [ ] **Band Ordering:** Is the channel order (RGB vs BGR vs NIR-R-G) consistent with your model's expected input?
    - *Risk:* OpenCV reads as BGR, Matplotlib reads as RGB, PyTorch expects (N, C, H, W). Mixing these leads to silent failures (model trains but performs poorly).
    - *Action:* Enforce explicit checks (e.g., `assert image.shape[0] == 3`) and visualize inputs before feeding to the model.