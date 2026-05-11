import os
import sys
import requests
import datetime

# Konfigurace
BASE_URL = "https://xmetrics.dev/reports"
ROOT_DIR = "REPORTS"

def download_file(url, local_path):
    """Stáhne soubor a uloží ho."""
    try:
        response = requests.get(url, timeout=20, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            content = response.content.decode("utf-8")
            with open(local_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            print(f"✅ Staženo: {os.path.basename(local_path)}")
            return True
        else:
            print(f"❌ Nenalezeno: {url} (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"⚠️ Chyba při stahování: {e}")
        return False

def download_reports(target_date):
    """Hlavní funkce pro stažení reportů pro konkrétní datum."""
    if not target_date:
        sys.exit(1)

    target_dir = os.path.join(ROOT_DIR, target_date)
    os.makedirs(target_dir, exist_ok=True)

    success_count = 0
    print(f"🚀 Cílové datum (pátek): {target_date}")

    # Stahování reportů R1 - R6
    for i in range(1, 7):
        remote_name = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{remote_name}"
        local_path = os.path.join(target_dir, f"R{i}.md")
        if download_file(url, local_path):
            success_count += 1

    # Stahování datasetu
    dataset_url = f"{BASE_URL}/{target_date}/D_{target_date}.csv"
    dataset_local_path = os.path.join(target_dir, "DATASET.csv")
    if download_file(dataset_url, dataset_local_path):
        success_count += 1

    if success_count == 0:
        print(f"\nℹ️ Žádné soubory pro datum {target_date} nebyly nalezeny.")
        # Neukončujeme chybou sys.exit(1), aby Action nebyla červená, když data ještě nejsou na webu
    else:
        print(f"\n✨ Hotovo! Celkem {success_count} souborů uloženo do {target_dir}.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].strip():
        # Pokud je datum zadáno ručně
        input_date = sys.argv[1]
    else:
        # AUTOMATIKA: Najde nejbližší minulý pátek
        today = datetime.date.today()
        # Vypočítá rozdíl k nejbližšímu pátku (pátek = 4. den v týdnu)
        days_to_subtract = (today.weekday() - 4) % 7
        
        # Pokud je dnes pátek, days_to_subtract bude 0 (stáhne dnešní). 
        # Pokud je úterý, days_to_subtract bude 4.
        target = today - datetime.timedelta(days=days_to_subtract)
        input_date = target.strftime("%Y-%m-%d")
        print(f"📅 Dnes je {today}, automaticky stahuji reporty pro pátek {input_date}")

    download_reports(input_date)
