import os
import json
import requests
from pathlib import Path

NEWS_DIR = Path("news")
API_URL = os.getenv("ROYAB_API_URL")
API_KEY = os.getenv("ROYAB_API_KEY")

if not API_URL or not API_KEY:
    raise RuntimeError("ROYAB_API_URL or ROYAB_API_KEY is not set")

json_files = sorted(NEWS_DIR.glob("*.json"))

if not json_files:
    print("No news files found.")
    raise SystemExit(0)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

for file_path in json_files:
    print(f"Publishing {file_path} ...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        print(f"Status: {response.status_code}")
        print(response.text)

        if response.status_code >= 200 and response.status_code < 300:
            file_path.unlink()
            print(f"Deleted published file: {file_path}")
        else:
            print(f"Failed to publish {file_path}, keeping file for retry.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
