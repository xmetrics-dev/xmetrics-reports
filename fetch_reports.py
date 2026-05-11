import os
import sys
import requests
import datetime

# Configuration
BASE_URL = "https://xmetrics.dev/reports"
ROOT_DIR = "REPORTS"

def download_file(url, local_path):
    """Downloads a file from a URL and saves it to a local path."""
    try:
        response = requests.get(url, timeout=20, stream=True)
        if response.status_code == 200:
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

    if os.path.exists(ROOT_DIR) and not os.path.isdir(ROOT_DIR):
        os.remove(ROOT_DIR)
    
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR, exist_ok=True)

    target_dir = os.path.join(ROOT_DIR, target_date)
    os.makedirs(target_dir, exist_ok=True)

    success_count = 0
    print(f"🚀 Starting download for targeted date: {target_date}")
    print(f"📂 Target directory: {target_dir}\n")

    for i in range(1, 7):
        remote_name = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{remote_name}"
        local_path = os.path.join(target_dir, f"R{i}.md")
        if download_file(url, local_path):
            success_count += 1

    dataset_url = f"{BASE_URL}/{target_date}/D_{target_date}.csv"
    dataset_local_path = os.path.join(target_dir, "DATASET.csv")
    if download_file(dataset_url, dataset_local_path):
        success_count += 1

    if success_count == 0:
        print(f"\n❌ No files were found for date {target_date}.")
        sys.exit(1)

    print(f"\n✨ Done! Total {success_count} files saved to {target_dir}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If date is provided manually via argument
        input_date = sys.argv[1]
    else:
        # Automatic mode: Take today's date and subtract 2 days (Sunday -> Friday)
        today = datetime.date.today()
        target = today - datetime.timedelta(days=4)
        input_date = target.strftime("%Y-%m-%d")
        print(f"📅 Automation: Today is {today}, targeting Friday's data ({input_date})")

    download_reports(input_date)
