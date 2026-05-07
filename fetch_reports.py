import os
import sys
import requests

BASE_URL = "https://xmetrics.dev/reports"

def download_reports(target_date):
    if not target_date:
        print("❌ Chyba: Nebylo zadáno žádné datum!")
        sys.exit(1)

    target_dir = os.path.join("Reporty", target_date)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    success_count = 0
    for i in range(1, 7):
        filename = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{filename}"
        
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                local_name = f"R{i}.md"
                with open(os.path.join(target_dir, local_name), "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"✅ Staženo: {local_name}")
                success_count += 1
            else:
                print(f"❌ Nenalezeno: {filename} (Status {response.status_code})")
        except Exception as e:
            print(f"⚠️ Chyba u {filename}: {e}")

    if success_count == 0:
        sys.exit(1)

if __name__ == "__main__":
    input_date = sys.argv[1] if len(sys.argv) > 1 else None
    download_reports(input_date)
