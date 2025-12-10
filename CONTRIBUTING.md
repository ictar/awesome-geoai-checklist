# Contributing to Awesome GeoAI Checklist

First off, thank you for considering contributing to `awesome-geoai-checklist`\! 🎉

This project is community-driven. Remote Sensing and GeoAI are complex fields, and no single person knows every potential pitfall. By sharing your hard-earned lessons, you are saving hours (or weeks) of debugging time for researchers and engineers around the world.

## 🤝 How Can You Contribute?

We welcome contributions of all forms:

1.  **Add a New Checklist Item:** Found a specific trap in SAR processing? Or a subtle bug in fine-tuning Prithvi/SatMAE? Add it\!
2.  **Improve Descriptions:** Clarify existing points or add better examples.
3.  **Add References:** Link to papers or documentation that prove *why* a certain step is necessary.
4.  **Python Utilities:** Submit scripts to `utils/` that automate these checks.
5.  **Fix Typo/Grammar:** Small fixes are always appreciated.

## 📝 Contribution Guidelines

To keep this repository high-quality and readable, please follow these rules when adding new items.

### 1. The Content Format

Every checklist item should follow this structure:

  - **Title:** Bold and concise.
  - **Description:** Explain the issue clearly.
  - **Context/Action:** (Optional but recommended) Explain *why* this matters or *how* to fix it.

**Example:**

```markdown
- [ ] **Pixel Alignment:** Are pixels from different sensors aligned to the exact same grid?
    - *Risk:* Sub-pixel misalignment causes noise in multi-modal fusion.
    - *Action:* Use `gdalwarp -tap` (Target Aligned Pixels) or `rasterio` realignment.
```

### 2. Scientific Validity

Since this is a scientific resource, please ensure your contributions are technically accurate.

  * **Avoid:** "I feel like Adam optimizer is bad."
  * **Prefer:** "Adam optimizer may cause instability in early training of ViTs on small datasets; consider using SGD or warmup." (Ideally with a reference).

### 3\. Directory Structure

  * **General Pitfalls:** Go to `checklists/00_general_principles.md`.
  * **Classification:** Go to `checklists/01_classification.md`.
  * **New Topics:** If you are adding a completely new domain (e.g., Object Detection), please discuss it in an Issue first, or create a new file like `checklists/03_detection.md`.

## 🚀 Pull Request Process

1.  **Fork** the repository to your own GitHub account.
2.  **Clone** the project to your machine.
3.  Create a **branch** locally with a concise name:
    ```bash
    git checkout -b add-sar-checklist
    ```
4.  **Commit** changes to the branch.
5.  **Push** changes to your fork.
6.  Open a **Pull Request** in our repository.

## 🐍 Contributing to `utils/`

If you are contributing a Python script:

  * Keep dependencies minimal (e.g., `rasterio`, `geopandas`, `numpy`, `torch`).
  * Add a simple docstring explaining what the script checks.
  * Ensure the code is readable.

-----

Thank you for making GeoAI research more robust\! 🌍

