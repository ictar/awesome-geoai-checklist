# Contributing to Awesome GeoAI Checklist

First off, thank you for considering contributing to `awesome-geoai-checklist`! 🎉

This project is community-driven. By sharing your hard-earned lessons, you are saving hours of debugging time for researchers around the world.

## ⚠️ Important: Strict Formatting Required

To keep this project useful, we use a script (`utils/generate_excel.py`) to automatically convert these Markdown files into Excel spreadsheets for project tracking.

**Your Pull Request MUST follow the specific format below, or the Excel generation will fail.**

### The Checklist Item Format

Every item must follow this exact structure. Please copy-paste this template:

```markdown
- [ ] **Item Title:** Short description or question?
    - *Risk/Context:* Explain WHY this is a problem.
    - *Action:*
        - Step 1 to fix it.
        - Step 2 to fix it.
    - *Tools:* `python utils/script_name.py` (Optional)
````

#### 🚨 Syntax Rules (Do not break these):

1. **Keywords:** You must use `*Risk:*`, `*Context:*`, `*Action:*`, and `*Tools:*` exactly as written (Italicized, followed by a colon).
2. **Indentation:** The keywords must be indented (4 spaces or 1 tab) under the main bullet point.
3. **Sub-bullets:** If an Action has multiple steps, use a sub-list (indent again + `-`). The parser will convert these into bullet points in the Excel cell.

-----

## 🤝 How Can You Contribute?

1. **Add a New Checklist Item:** Found a specific trap in SAR processing? Or a subtle bug in fine-tuning Prithvi/SatMAE? Add it\!
2. **Add References:** Link to papers or documentation that prove *why* a certain step is necessary.
3. **Python Utilities:** Submit scripts to `utils/` that automate these checks.
4. **Fix Typo/Grammar:** Small fixes are always appreciated.

## 📝 Scientific Validity Guidelines

Since this is a scientific resource, please ensure your contributions are technically accurate.

* **Avoid:** "I feel like Adam optimizer is bad."
* **Prefer:** "Adam optimizer may cause instability in early training of ViTs on small datasets; consider using SGD or warmup." (Ideally with a reference).
* **Scope:** Keep items relevant to Geospatial/Remote Sensing specific challenges, or general ML pitfalls that are particularly fatal in GeoAI.

## 🚀 Pull Request Process

1. **Fork** the repository to your own GitHub account.
2. **Clone** the project to your machine.
3. Create a **branch** locally with a concise name: `git checkout -b add-sar-checklist`W
4. **Test the Parser:** Before pushing, run `python utils/generate_excel.py` to ensure your new items appear correctly in the Excel file.
5. **Commit & Push** changes.
6. Open a **Pull Request**.

-----

Thank you for making GeoAI research more robust! 🌍