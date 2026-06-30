import os
import requests
from tqdm import tqdm
from pathlib import Path

DATASETS = [
    {
        "name": "NASA CMAPSS",
        "url": "https://data.nasa.gov/download/cmapss-jet-engine-simulated-data.csv",
        "size": "~3 GB (compressed CSV)",
        "license": "Public Domain (NASA)",
        "target": "data/raw/nasa_cmapss.csv"
    },
    {
        "name": "ACN Charging Dataset",
        "url": "https://ev.caltech.edu/dataset/ACN_charging_data.zip",
        "size": "~2.5 GB",
        "license": "CC-BY-4.0 (citation required)",
        "target": "data/raw/acn_charging.zip"
    },
    {
        "name": "Battery Archive",
        "url": "https://batteryarchive.org/download/latest_battery_dataset.zip",
        "size": "~1.8 GB",
        "license": "CC-BY-4.0",
        "target": "data/raw/battery_archive.zip"
    },
    {
        "name": "ElaadNL EV Dataset",
        "url": "https://platform.elaad.io/analyses-data/download",
        "size": "~1 GB (requires free registration)",
        "license": "Open Data (ELAA-NL)",
        "target": "data/raw/elaadnl_ev.zip"
    },
    {
        "name": "GSCPI Supply Chain Index",
        "url": "https://www.newyorkfed.org/medialibrary/media/research/policy/gscpi/gscpi.csv",
        "size": "~12 MB",
        "license": "Public Domain (Federal Reserve)",
        "target": "data/raw/gscpi.csv"
    },
    {
        "name": "UNCTAD Maritime Dataset",
        "url": "https://datadashboard.unctad.org/transport-and-trade/maritime/download",
        "size": "~150 MB",
        "license": "Open Data (UNCTAD)",
        "target": "data/raw/unctad_maritime.csv"
    }
]

def download_file(url, dest_path, expected_size=None):
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True, timeout=30)
    total = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024  # 1 MB
    tqdm_bar = tqdm(total=total, unit='iB', unit_scale=True, desc=dest_path.name)
    with open(dest_path, 'wb') as f:
        for data in response.iter_content(block_size):
            tqdm_bar.update(len(data))
            f.write(data)
    tqdm_bar.close()
    if total != 0 and dest_path.stat().st_size != total:
        print(f"Warning: downloaded size for {dest_path.name} does not match expected size.")

def main():
    for ds in DATASETS:
        print(f"[INFO] {ds['name']}")
        print(f"  URL       : {ds['url']}")
        print(f"  Size      : {ds['size']}")
        print(f"  License   : {ds['license']}")
        print(f"  Target    : {ds['target']}")
        try:
            download_file(ds['url'], ds['target'])
            print(f"[SUCCESS] Downloaded {ds['name']} to {ds['target']}")
        except Exception as e:
            print(f"[ERROR] Failed to download {ds['name']}: {e}")
            print("Manual download instructions:")
            print(f"  • Open a browser and go to: {ds['url']}")
            print(f"  • Save the file to: {ds['target']}")
            return  # stop on first failure as requested

if __name__ == "__main__":
    main()
