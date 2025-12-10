"""
Utility to check class stratification across Train, Val, and Test datasets.
Verifies if the class distribution is consistent across splits.
Usage example:
    python utils/check_distribution.py --train train.geojson --val val.geojson --test test.geojson --col landcover_id
"""
import geopandas as gpd
import pandas as pd
import argparse
import sys

def check_class_balance(train_path, val_path, test_path, label_col):
    """
    Verifies class distribution (Counts & Percentages) across Train, Val, and Test splits.
    """
    print("Loading datasets...")
    try:
        datasets = {
            'Train': gpd.read_file(train_path),
            'Val':   gpd.read_file(val_path),
            'Test':  gpd.read_file(test_path)
        }
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        sys.exit(1)

    # Calculate Totals
    totals = {name: len(df) for name, df in datasets.items()}
    
    print(f"\n📊 DISTRIBUTION REPORT (Label: '{label_col}')")
    print("="*105)
    # Header with Total Counts
    header = f"{'Class':<15} | {'Train (N=' + str(totals['Train']) + ')':<22} | {'Val (N=' + str(totals['Val']) + ')':<22} | {'Test (N=' + str(totals['Test']) + ')':<22} | {'Status':<10}"
    print(header)
    print("-" * 105)

    # Get all unique classes sorted
    all_classes = set()
    for name, df in datasets.items():
        if label_col not in df.columns:
            print(f"❌ Error: Column '{label_col}' not found in {name} dataset.")
            sys.exit(1)
        all_classes.update(df[label_col].unique())
    
    all_classes = sorted(list(all_classes))
    
    warning_flag = False
    
    for cls in all_classes:
        row_str = f"{str(cls):<15} | "
        percentages = {}
        
        # Calculate stats for each split
        for name in ['Train', 'Val', 'Test']:
            df = datasets[name]
            count = len(df[df[label_col] == cls])
            total = totals[name]
            
            if total > 0:
                pct = (count / total) * 100
            else:
                pct = 0.0
            
            percentages[name] = pct
            
            # Format: "Count (Pct%)" -> e.g., "150 (15.2%)"
            cell_content = f"{count} ({pct:.1f}%)"
            row_str += f"{cell_content:<22} | "

        # Logic Check: Variance > 5% or Missing Class
        t_pct, v_pct, te_pct = percentages['Train'], percentages['Val'], percentages['Test']
        max_diff = max(abs(t_pct - v_pct), abs(t_pct - te_pct))
        
        status = "✅ OK"
        if max_diff > 5.0:
            status = "⚠️ SKEWED"
            warning_flag = True
        
        # Check for zero samples in any split
        if t_pct == 0 or v_pct == 0 or te_pct == 0:
            status = "❌ MISSING"
            warning_flag = True

        row_str += f"{status:<10}"
        print(row_str)

    print("-" * 105)
    
    # Final Summary
    print(f"Total Samples: {sum(totals.values())}")
    if warning_flag:
        print("\n❌ ISSUE DETECTED: Class distributions are skewed (>5% diff) or classes are missing in some splits.")
        print("   Action: Re-split your data using Stratified Sampling (e.g., sklearn stratify=y).")
    else:
        print("\n✅ SUCCESS: Class distributions are stratified and consistent.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check class stratification (Counts & %) across splits.")
    parser.add_argument("--train", required=True, help="Train file path (shp/geojson)")
    parser.add_argument("--val", required=True, help="Validation file path (shp/geojson)")
    parser.add_argument("--test", required=True, help="Test file path (shp/geojson)")
    parser.add_argument("--col", required=True, help="Name of the label/class column")

    args = parser.parse_args()
    
    check_class_balance(args.train, args.val, args.test, args.col)