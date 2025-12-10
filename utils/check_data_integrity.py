"""
Utility to check data integrity of raster datasets.
Scans a directory of rasters to check for CRS consistency and NoData values.
Usage example:
    python utils/check_data_integrity.py --dir path/to/rasters --crs EPSG:32649
"""
import rasterio
import glob
import argparse
import os

def check_integrity(raster_dir, ref_crs=None):
    """
    Scans a directory of rasters to check for CRS consistency and NoData values.
    """
    tif_files = glob.glob(os.path.join(raster_dir, "*.tif"))
    if not tif_files:
        print("No .tif files found.")
        return

    print(f"🔍 Scanning {len(tif_files)} rasters in {raster_dir}...")
    
    issues = []
    first_crs = None
    
    for f in tif_files:
        with rasterio.open(f) as src:
            # 1. CRS Consistency
            if first_crs is None:
                first_crs = src.crs
                if ref_crs and str(src.crs) != str(ref_crs):
                     issues.append(f"{os.path.basename(f)}: CRS mismatch with reference (Found {src.crs})")
            elif src.crs != first_crs:
                issues.append(f"{os.path.basename(f)}: CRS mismatch (Found {src.crs}, expected {first_crs})")
            
            # 2. NoData Check
            if src.nodata is None:
                 issues.append(f"{os.path.basename(f)}: NoData value is NOT defined in metadata.")

    print("\n" + "="*30)
    print("INTEGRITY REPORT")
    print("="*30)
    
    if not issues:
        print(f"✅ All files consistent.")
        print(f"   CRS: {first_crs}")
    else:
        print(f"❌ Found {len(issues)} issues:")
        for i in issues:
            print(f"   - {i}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directory containing .tif images")
    parser.add_argument("--crs", default=None, help="Optional: Expected EPSG code (e.g. EPSG:32649)")
    args = parser.parse_args()
    
    check_integrity(args.dir, args.crs)