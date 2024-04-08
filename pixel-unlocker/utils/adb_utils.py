import os
import zipfile
import requests
import subprocess
from pathlib import Path

ADB_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
ADB_DIR = Path(__file__).parent.parent / "adb"  # Adjust the path according to your project structure

def download_and_extract_adb():
    if not ADB_DIR.exists():
        ADB_DIR.mkdir(parents=True, exist_ok=True)
        print("Downloading ADB...")
        response = requests.get(ADB_URL, stream=True)
        zip_path = ADB_DIR / "platform-tools-latest-windows.zip"
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Extracting ADB...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ADB_DIR)

def get_adb_path():
    # Check if ADB exists in the project directory first
    local_adb_path = ADB_DIR / "platform-tools" / "adb.exe"
    if local_adb_path.exists():
        return str(local_adb_path)
    # Fall back to checking the system PATH
    try:
        subprocess.run(["adb", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "adb"  # If this succeeds, use ADB from system PATH
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def setup_adb():
    adb_path = get_adb_path()
    if not adb_path:
        download_and_extract_adb()
        return str(ADB_DIR / "platform-tools" / "adb.exe")
    return adb_path

def execute_adb_command(command):
    adb_path = setup_adb()
    if not adb_path:
        raise RuntimeError("Failed to set up ADB")
    
    full_command = [adb_path] + command if adb_path != "adb" else command
    process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()
