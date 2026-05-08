import os
import sys
import requests

BASE_URL = "https://xmetrics.dev/reports"


def download_reports(target_date):
    if not target_date:
        print("❌ Chyba: Nebylo zadáno žádné datum!")
        sys.exit(1)

    target_dir = os.path.join("Reporty", target_date)
    os.makedirs(target_dir, exist_ok=True)

    success_count = 0

    for i in range(1, 7):
        filename = f"R{i}_{target_date}.md"
        url = f"{BASE_URL}/{target_date}/{filename}"

        try:
            response = requests.get(url, timeout=20)

            if response.status_code == 200:
                local_name = f"R{i}.md"
                local_path = os.path.join(target_dir, local_name)

                # RAW bytes -> explicit UTF-8 decode
                content = response.content.decode("utf-8")

                with open(local_path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)

                print(f"✅ Staženo: {local_name}")
                success_count += 1

            else:
                print(f"❌ Nenalezeno: {filename} (Status {response.status_code})")

        except UnicodeDecodeError as e:
            print(f"⚠️ UTF-8 decode chyba u {filename}: {e}")

        except requests.RequestException as e:
            print(f"⚠️ HTTP chyba u {filename}: {e}")

        except Exception as e:
            print(f"⚠️ Neočekávaná chyba u {filename}: {e}")

    if success_count == 0:
        print("❌ Nepodařilo se stáhnout žádný report.")
        sys.exit(1)

    print(f"\n✅ Hotovo. Staženo {success_count} reportů.")


if __name__ == "__main__":
    input_date = sys.argv[1] if len(sys.argv) > 1 else None
    download_reports(input_date)
