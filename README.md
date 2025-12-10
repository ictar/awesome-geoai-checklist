# 🌍 Awesome GeoAI Checklist

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **A curated, community-driven checklist to ensure robustness and correctness in Geospatial AI & Remote Sensing workflows.**

Remote Sensing (RS) and GeoAI differ fundamentally from general Computer Vision. Ignoring spatial autocorrelation, coordinate systems, or sensor characteristics often leads to **"fake high accuracy"** (data leakage) or models that fail in production.

This repository aims to be the **standard pre-flight check** for researchers and engineers.

## 📚 Checklist Index

### 🟢 Phase 1: The Essentials (Read First)
Before model training, ensure your data foundation is solid.
* [**General Principles & Data Integrity**](./checklists/00_general_principles.md)
    * *Includes: CRS alignment, Spatial Splitting (The Golden Rule), NoData handling.*

### 🔵 Phase 2: Task-Specific Checklists
Select the checklist that matches your downstream task.
* [**Classification (Multi-class / Multi-label)**](./checklists/01_classification.md)
    * *Focus: Activation functions, Class imbalance, Foundation Model Fine-tuning.*


## 🛠️ Diagnostics Toolkit

We provide Python scripts in the [`utils/`](./utils/) directory to help you automatically pass these checks.

### 📊 Export to Excel (Project Tracker)
Turn these markdown checklists into a professional Excel spreadsheet for project management or delivery.
```bash
python utils/generate_excel.py
```
*Output: `GeoAI_Checklist.xlsx` with columns for Risk, Action, Tools, and Status.*

## 🤝 Contributing

Found a new pitfall? Learned a hard lesson? Please share it!
Check [CONTRIBUTING.md](CONTRIBUTING.md) to submit a Pull Request.
