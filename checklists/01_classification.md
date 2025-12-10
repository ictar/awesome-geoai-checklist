# Classification Checklist

> **Scope:** Image Classification (Scene-level) & Pixel-wise Classification.
> **Includes:** Deep Learning (CNNs/ViTs) & Traditional ML (RF, SVM, XGBoost).


## 1. Data Splitting Strategy (The Foundation)
*Crucial steps before training begins.*

- [ ] **Stratified Split (Mandatory):** Did you use stratified sampling when splitting Train/Test sets?
    - *Risk:* Random splitting on imbalanced data causes "class disappearance" (e.g., the rare class ends up entirely in Train, leaving 0 samples in Test).
    - *Action:* 
      - Use parameters like `stratify=y` in Scikit-learn to ensure Class A:B:C ratios are identical across Train, Validation, and Test sets. 
      - **Explicitly print the class counts (or histograms)** for Train, Val, and Test sets. Verify that the *percentage* of each class is roughly identical across all three sets.
    - *Tools:* `utils/check_distribution.py`
- [ ] **The "Three-Way" Split (Val != Test):** Do you have three distinct sets: **Train** (Weights), **Validation** (Hyperparameters), and **Test** (Final Evaluation)?
    - *Risk:* Reporting metrics based on the Validation set leads to biased, inflated results because you "tuned" the model to fit that specific data.
    - *Action:* The **Test Set** must be locked away (unseen) until the final manuscript/report generation.

## 2. General Model Configuration
*Applies to both DL and Traditional ML.*

- [ ] **Class Imbalance Strategy:** Are you handling the skewed distribution of geospatial classes?
    - *Risk:* Models will default to predicting the majority class (e.g., "Water" everywhere) to maximize Accuracy, ignoring small but important classes.
    - *Action:* Use `class_weight='balanced'` (sklearn) or `WeightedRandomSampler` / Weighted Loss (PyTorch). Report **Macro-F1** instead of Accuracy.
    - *Tools:* `python utils/check_distribution.py` (Helps identify imbalance severity)
- [ ] **Confusion Matrix:** Have you inspected *which* classes are being confused? (e.g., differentiating "Shadow" from "Water").
    - *Context:* Global metrics hide specific failure modes (e.g., "Shadow" being misclassified as "Water").
    - *Action:* Plot the matrix and look for high values off the diagonal.
- [ ] **Baseline Comparison:** Does your model outperform a "Dummy Classifier" (which always predicts the majority class)?
    - *Risk:* Complex models might achieve 90% accuracy, but if the majority class is 90% of the data, the model has learned nothing.
    - *Action:* Compare your results against a baseline that always predicts the most frequent class.

## 3. Traditional ML Specifics (RF, SVM, XGBoost)
*Specific checks for non-deep learning approaches.*

### Feature Engineering & Preprocessing
- [ ] **Feature Scaling:** If using distance-based models (SVM, KNN, MLP), are features scaled to `[0, 1]` or Standardized (Mean=0, Std=1)?
    - *Risk:* Raw satellite DN values (e.g., 0-10000) will dominate derived indices (e.g., NDVI 0-1) in distance-based calculations, making the model ignore valid features.
    - *Action:* Apply `StandardScaler` or `MinMaxScaler` before training. (Less critical for Random Forest, but mandatory for others).
- [ ] **Encoding Categorical Features:** Are categorical features encoded correctly for your model type?
    - *Risk:* Using Label Encoding (0, 1, 2) for linear models (SVM, Logistic Regression) implies an ordinal relationship ($2 > 1$) which introduces bias.
    - *Action:* Use **One-Hot Encoding** for linear models; Label Encoding is acceptable for Tree-based models.

### Evaluation Traps
- [ ] **The "[OOB Error](https://en.wikipedia.org/wiki/Out-of-bag_error)" Trap (Random Forest):** Are you relying solely on Random Forest's Out-Of-Bag (OOB) score?
    - *Risk:* **Spatial Autocorrelation.** OOB samples are often geographically adjacent to Training samples, leading to a severely inflated accuracy score that fails in practice.
    - *Action:* Ignore OOB for accuracy reporting; always use an external, spatially separated Test Set.
- [ ] **Dimensionality Reduction:** Have you handled the "Curse of Dimensionality" (e.g., Hyperspectral data)?
    - *Risk:* With limited samples and hundreds of bands, classifiers (especially SVM) struggle to generalize (Hughes phenomenon).
    - *Action:* Perform PCA or Recursive Feature Elimination (RFE) to reduce bands before training.

## 4. Deep Learning Configuration
*Specific checks for CNNs, ViTs, etc.*

### Activation & Loss Logic
| Task Type | Logic | Correct Activation | Correct Loss |
| :--- | :--- | :--- | :--- |
| **Multi-Class** | Mutually Exclusive | `Softmax` | Cross Entropy (CE) |
| **Multi-Label** | Co-occurring | `Sigmoid` | Binary Cross Entropy (BCE) |

- [ ] **Check:** Does your model's final layer match the table above?
  - *Risk:* Using `Softmax` for multi-label tasks prevents the model from predicting multiple classes simultaneously.

## 5. Foundation Model Fine-Tuning (Geo-FM)
*Specific checks for Pre-trained Models (Prithvi, SatMAE, ResNet, etc.).*

- [ ] **Input Normalization:** Which Mean/Std statistics are you using?
    - *Risk:* Using the current dataset's stats while keeping the backbone frozen causes a distribution shift, rendering pre-trained weights ineffective.
    - *Action:*
      - *Frozen Weights:* Must use the pre-trained model's original Mean/Std.
      - *Full Fine-tuning:* Can use current dataset's Mean/Std (but careful with domain shift).
- [ ] **Resolution (GSD) Gap:** Is the input resolution similar to the pre-training data?
    - *Risk:* A model pre-trained on 30m Landsat data may fail to extract features from 0.5m Aerial imagery due to scale differences.
    - *Action:* Resize inputs or use patch interpolation to bridge the Ground Sampling Distance (GSD) gap.
- [ ] **Channel Adaptation:** How are extra spectral bands handled?
    - *Risk:* Force-feeding 12 bands into a 3-channel RGB backbone results in dimension mismatch errors or information loss.
    - *Action:* Initialize a learnable `1x1 Conv` layer to project N channels to 3, or use PCA to select top 3 components.

- [ ] **Overfitting (Capacity Mismatch):** Are you preventing the massive model from memorizing your small dataset?
    - *Context:* Geo-Foundation models have millions of parameters. Downstream tasks often have few samples.
    - *Risk:* The model achieves 99% Training Accuracy but fails on Test data (Overfitting).
    - *Action:*
        1. **Freeze the Backbone:** Start by training *only* the classification head ([Linear Probing](https://en.wikipedia.org/wiki/Linear_probing)).
        2. **PEFT:** Use Parameter-Efficient Fine-Tuning methods like **LoRA** or Adapters instead of full fine-tuning.
        3. **Early Stopping:** Monitor Validation Loss strictly and stop when it degrades.

## 6. Sanity Checks
*Quick tests to verify code logic.*

- [ ] **The "Overfit" Test:** Can the model reach ~0 loss (or 100% accuracy) on a **single batch**? (Verifies code correctness).
    - *Risk:* If a model cannot memorize 10 images, there is a bug in the code, data loader, or labels.
    - *Action:* Run a quick training loop on a tiny subset before full training.
- [ ] **The "Nearest Neighbor" Test:** Are Test set images visually distinct from Training set images? (Manual inspection for leakage).
    - *Risk:* Metrics look great, but the model is just memorizing near-duplicates (Spatial Leakage).
    - *Action:* Manually inspect the nearest neighbor in Training set for a few Test samples.
