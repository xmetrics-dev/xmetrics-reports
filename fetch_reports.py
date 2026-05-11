import os
import sys
import requests

# Configuration
BASE_URL = "https://xmetrics.dev/reports"
ROOT_DIR = "REPORTS"

def download_file(url, local_path):
    """Downloads a file from a URL and saves it to a local path."""
    try:
        # Using stream=True for better handling of large files
        response = requests.get(url, timeout=20, stream=True)

        if response.status_code == 200:
            # Ensure the directory for the file exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            content = response.content.decode("utf-8")
            with open(local_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

            print(f"✅ Downloaded: {os.path.basename(local_path)}")
            return True
        else:
            print(f"❌ Not Found: {url} (Status {response.status_code})")
            return False

    except Exception as e:
        print(f"⚠️ Error downloading {os.path.basename(local_path)}: {e}")
        return False


def download_reports(target_date):
    """Main function to download reports and the dataset for a specific date."""
    if not target_date:
        print("❌ Error: No date provided!")
        sys.exit(1)

    # Building the path: REPORTS/YYYY-MM-DD
    target_dir = os.path.join(ROOT_DIR, target_date)

    # Critical fix: If a FILE named 'REPORTS' exists, remove it to prevent NotADirectoryError
    if os.path.exists(ROOT_DIR) and not os.path.isdir(ROOT_DIR):
        print(f"⚠️ Warning: Found a file named '{ROOT_DIR}' blocking directory creation. Removing it...")
        os.remove(ROOT_DIR)

    # Create the directory structure (creates both ROOT_DIR and the date subfolder)
    os.makedirs(target_dir, exist_ok=True)

    success_count = 0

    print(f"🚀 Starting download for date: {target_date}")
    print(f"📂 Target directory: {target_dir}\n")

    # =============================================================
    # 1. REPORTS R1 to R6
    # =============================================================
    for i in range(1, 7):
        remote_name = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{remote_name}"

        local_name = f"R{i}.md"
        local_path = os.path.join(target_dir, local_name)

        if download_file(url, local_path):
            success_count += 1

    # =============================================================
    # 2. DATASET (CSV)
    # =============================================================
    dataset_remote = f"D_{target_date}.csv"
    dataset_url = f"{BASE_URL}/{target_date}/{dataset_remote}"

    dataset_local = "DATASET.csv"
    dataset_local_path = os.path.join(target_dir, dataset_local)

    if download_file(dataset_url, dataset_local_path):
        success_count += 1

    # =============================================================
    # RESULT SUMMARY
    # =============================================================
    if success_count == 0:
        print(f"\n❌ No files were downloaded for date {target_date}.")
        sys.exit(1)

    print(f"\n✨ Done! Total {success_count} files saved to {target_dir}.")


if __name__ == "__main__":
    # Expects date as the first argument (e.g., python fetch_reports.py 2026-05-12)
    input_date = sys.argv[1] if len(sys.argv) > 1 else None
    download_reports(input_date)
