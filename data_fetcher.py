#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
import requests
import pandas as pd

# =========================================================
# CONFIG
# =========================================================

MAPBOX_TOKEN = "pk.eyJ1Ijoic2F1bXlhYmhhcnRpIiwiYSI6ImNtamZvOWdmaDBzNzYzY3NsY3N1NzJsa3EifQ.vEwUmpq4I2TOd3pjAdflJg"  # <-- put your token here

CSV_PATH = "test.csv"    # path to your tabular data
IMAGE_DIR = "data/images/test"

ZOOM = 16
IMAGE_SIZE = 256

SLEEP_TIME = 0.3            # seconds between requests
RETRIES = 5                 # retry attempts per image
TIMEOUT = 10                # seconds


# =========================================================
# FUNCTION TO FETCH ONE IMAGE
# =========================================================

def fetch_satellite_image(
    lat,
    lon,
    save_path,
    zoom=ZOOM,
    size=IMAGE_SIZE,
    retries=RETRIES,
    timeout=TIMEOUT
):
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
        f"{lon},{lat},{zoom}/{size}x{size}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return True

            elif response.status_code == 429:
                print("Rate limited. Sleeping longer...")
                time.sleep(2)

            else:
                print(f" HTTP {response.status_code} for {save_path}")

        except requests.exceptions.Timeout:
            print(" Timeout. Retrying...")

        except requests.exceptions.RequestException as e:
            print(f" Network error: {e}")

        time.sleep(1 + attempt)  # exponential backoff

    print(f" Failed after retries: {save_path}")
    return False


# =========================================================
# MAIN SCRIPT
# =========================================================

def main():
    # Load tabular data
    df = pd.read_csv(CSV_PATH)

    # Create image directory
    os.makedirs(IMAGE_DIR, exist_ok=True)

    print(f" Total samples: {len(df)}")
    print(" Starting image download...\n")

    for idx, row in df.iterrows():
        save_path = os.path.join(IMAGE_DIR, f"{idx}.png")

        # Skip if already downloaded (resume-safe)
        if os.path.exists(save_path):
            continue

        lat = row["lat"]
        lon = row["long"]

        success = fetch_satellite_image(lat, lon, save_path)

        if not success:
            print(f" Skipping index {idx}")

        time.sleep(SLEEP_TIME)

    print("\n Image download completed.")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()

