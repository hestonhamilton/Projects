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

    full_command = [os.path.join(adb_path, 'adb.exe')] + command if adb_path != "adb" else ['adb'] + command
    process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"ADB command {command} failed: {stderr}")
    return stdout.decode().strip()

def execute_fastboot_command(command):
    fastboot_path = setup_adb()
    if not fastboot_path:
        raise RuntimeError("Failed to set up Fastboot")

    full_command = [os.path.join(fastboot_path, 'fastboot.exe')] + command if fastboot_path != "adb" else ['fastboot'] + command
    process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"Fastboot command {command} failed: {stderr}")
    return stdout.decode().strip()

def get_connected_devices():
    _, stdout, _ = execute_adb_command(["devices"])
    devices = []
    for line in stdout.splitlines():
        if "\tdevice" in line:
            device_id = line.split("\t")[0]
            devices.append(device_id)
    return devices
    
def get_firmware_details(device_id):
    version_release = execute_adb_command(["-s", device_id, "shell", "getprop", "ro.build.version.release"]).strip()
    build_id = execute_adb_command(["-s", device_id, "shell", "getprop", "ro.build.id"]).strip()
    
    return version_release, build_id

def get_device_model(device_id):
    command = ["shell", "getprop", "ro.product.model"]
    _, model, _ = execute_adb_command(["-s", device_id] + command)
    return model.strip()

def reboot_device(device_id):
    execute_fastboot_command(["-s", device_id, "reboot"])