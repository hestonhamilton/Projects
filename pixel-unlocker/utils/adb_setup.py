#!/usr/bin/env python3
import os
import zipfile
import requests
import subprocess
from pathlib import Path

ADB_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
ADB_DIR = Path.home() / "adb"

def download_adb():
    print("Downloading ADB...")
    response = requests.get(ADB_URL, stream=True)
    with open("platform-tools-latest-windows.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def extract_adb():
    print("Extracting ADB...")
    with zipfile.ZipFile("platform-tools-latest-windows.zip", 'r') as zip_ref:
        zip_ref.extractall(str(ADB_DIR))

def add_adb_to_path():
    print("Adding ADB to PATH...")
    os.environ["PATH"] += os.pathsep + str(ADB_DIR / "platform-tools")
    # You may also want to add this path to the system's environment variables permanently

def is_adb_installed():
    try:
        subprocess.run(["adb", "--version"], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_adb():
    if not is_adb_installed():
        download_adb()
        extract_adb()
        add_adb_to_path()
        print("ADB setup complete.")
    else:
        print("ADB is already installed.")

if __name__ == "__main__":
    setup_adb()
