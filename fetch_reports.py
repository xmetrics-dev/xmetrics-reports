import os
import sys
import requests

BASE_URL = "https://xmetrics.dev/reports"


def download_file(url, local_path):
    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            content = response.content.decode("utf-8")

            with open(local_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

            print(f"✅ Staženo: {os.path.basename(local_path)}")
            return True

        else:
            print(f"❌ Nenalezeno: {url} (Status {response.status_code})")
            return False

    except UnicodeDecodeError as e:
        print(f"⚠️ UTF-8 decode chyba: {e}")

    except requests.RequestException as e:
        print(f"⚠️ HTTP chyba: {e}")

    except Exception as e:
        print(f"⚠️ Neočekávaná chyba: {e}")

    return False


def download_reports(target_date):
    if not target_date:
        print("❌ Chyba: Nebylo zadáno žádné datum!")
        sys.exit(1)

    target_dir = os.path.join("REPORTS", target_date)
    os.makedirs(target_dir, exist_ok=True)

    success_count = 0

    # =========================
    # REPORTY R1-R6
    # =========================
    for i in range(1, 7):
        remote_name = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{remote_name}"

        local_name = f"R{i}.md"
        local_path = os.path.join(target_dir, local_name)

        if download_file(url, local_path):
            success_count += 1

    # =========================
    # DATASET D_YYYY-MM-DD.md
    # =========================
    dataset_remote = f"D_{target_date}.csv"
    dataset_url = f"{BASE_URL}/{target_date}/{dataset_remote}"

    dataset_local = "DATASET.csv"
    dataset_local_path = os.path.join(target_dir, dataset_local)

    if download_file(dataset_url, dataset_local_path):
        success_count += 1

    # =========================
    # VÝSLEDEK
    # =========================
    if success_count == 0:
        print("❌ Nepodařilo se stáhnout žádné soubory.")
        sys.exit(1)

    print(f"\n✅ Hotovo. Staženo {success_count} souborů.")


if __name__ == "__main__":
    input_date = sys.argv[1] if len(sys.argv) > 1 else None
    download_reports(input_date)
