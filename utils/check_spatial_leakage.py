"""
Utility to check for spatial leakage between training and testing datasets.
Checks if any test samples are within a specified buffer distance of training samples.
Usage example:
    python check_spatial_leakage.py --train path/to/train.shp --test path/to/test.shp --buffer 100
"""
import geopandas as gpd
from sklearn.neighbors import BallTree
import numpy as np
import argparse

def check_spatial_leakage(train_path, test_path, buffer_dist=0):
    """
    Checks if Test samples are physically too close to Training samples.
    """
    print(f"Loading files...\n Train: {train_path}\n Test: {test_path}")
    
    # Load Data
    gdf_train = gpd.read_file(train_path)
    gdf_test = gpd.read_file(test_path)

    # 1. CRS Check
    if gdf_train.crs != gdf_test.crs:
        raise ValueError(f"CRS Mismatch! Train: {gdf_train.crs}, Test: {gdf_test.crs}")
    
    # Warning for Geographic CRS
    if gdf_train.crs.is_geographic:
        print("⚠️  WARNING: Data is in Lat/Lon (Degrees). Distances will be calculated in DEGREES, which is not recommended. Please project to UTM first.")

    print(f"Checking {len(gdf_test)} test samples against {len(gdf_train)} training samples...")

    # 2. Build Spatial Index (BallTree for fast query)
    # We use centroids in case inputs are polygons
    train_points = np.vstack([gdf_train.geometry.centroid.x, gdf_train.geometry.centroid.y]).T
    test_points = np.vstack([gdf_test.geometry.centroid.x, gdf_test.geometry.centroid.y]).T

    tree = BallTree(train_points, leaf_size=15)
    
    # 3. Query Nearest Neighbors
    # dists: distance to the nearest training sample for each test sample
    dists, _ = tree.query(test_points, k=1) 
    min_dists = dists.flatten()

    # 4. Report
    leakage_mask = min_dists <= buffer_dist
    num_leaks = np.sum(leakage_mask)
    
    print("\n" + "="*40)
    print("🔍 SPATIAL LEAKAGE REPORT")
    print("="*40)
    print(f"Minimum Distance Found: {np.min(min_dists):.2f}")
    print(f"Median Distance Found:  {np.median(min_dists):.2f}")
    
    if num_leaks > 0:
        print(f"\n❌ FAILED: Found {num_leaks} test samples within {buffer_dist} units of training data.")
        print(f"   Leakage Rate: {num_leaks / len(gdf_test) * 100:.2f}%")
        print("   -> Your split is likely Random, not Spatial.")
    else:
        print(f"\n✅ PASSED: No test samples found within {buffer_dist} units buffer.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for Spatial Leakage between Train and Test sets.")
    parser.add_argument("--train", type=str, required=True, help="Path to Training vector file (shp/geojson)")
    parser.add_argument("--test", type=str, required=True, help="Path to Test vector file (shp/geojson)")
    parser.add_argument("--buffer", type=float, default=0.0, help="Minimum allowed distance buffer (default 0)")
    
    args = parser.parse_args()
    
    check_spatial_leakage(args.train, args.test, args.buffer)