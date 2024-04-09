import requests
import os
from utils.adb_utils import execute_adb_command, get_firmware_details, get_device_model

def download_boot_img_for_pixel(device_id):
    # Get firmware details from the device
    version_release, build_id = get_firmware_details(device_id)

    # Identify the device model (modify the function to return the model)
    device_model = get_device_model(device_id)

    # Construct the download URL (adjust this based on how Google formats these URLs)
    base_url = "https://dl.google.com/dl/android/aosp/"
    file_name = f"{device_model}-{build_id}-factory.zip"
    download_url = f"{base_url}{file_name}"

    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download firmware for {device_model} with firmware {build_id}")

    # Save the firmware file
    boot_img_directory = os.path(__file__).parent / "boot_img"
    boot_img_directory.mkdir(exist_ok=True)

    boot_img_path = boot_img_directory / file_name

    with open(boot_img_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

    return boot_img_path



def download_latest_apk(repo_url):
    api_url = f"https://api.github.com/repos/{repo_url}/releases/latest"
    response = requests.get(api_url)
    response.raise_for_status()  # Raises an error for failed requests

    release_data = response.json()
    apk_download_info = next((asset for asset in release_data.get('assets', []) if asset['name'].endswith('.apk')), None)

    if not apk_download_info:
        raise RuntimeError("No APK found in the latest release.")

    apk_url = apk_download_info['browser_download_url']
    apk_name = apk_download_info['name']  # Retain the original file name

    # Define the directory where APKs will be saved
    apk_directory = os.path(__file__).parent / "apk"
    apk_directory.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

    apk_local_path = apk_directory / apk_name

    apk_response = requests.get(apk_url)
    apk_response.raise_for_status()

    with open(apk_local_path, "wb") as file:
        file.write(apk_response.content)

    return apk_local_path

def download_magisk_apk():
    download_latest_apk("https://github.com/topjohnwu/Magisk/releases")
    
def download_lsposed_apk():
    download_latest_apk("https://github.com/LSPosed/LSPosed/releases")
    
def download_safetynet_fix_apk():
    download_latest_apk("https://github.com/kdrag0n/safetynet-fix/releases")

def download_xposed_hidemocklocation_apk():
    download_latest_apk("https://github.com/Xposed-Modules-Repo/com.github.thepiemonster.hidemocklocation/releases")
    
#smalipatcher https://xdaforums.com/attachments/smalipatcher-0-0-7-4-fomey-xda-zip.5391111/

def copy_apk_to_device(device_id, apk_path):
    device_path = "/sdcard/Download/" + os.path.basename(apk_path)
    execute_adb_command(["-s", device_id, "push", apk_path, device_path])
    return device_path  # Returning the path where the APK was copied on the device

def install_apk_on_device(device_id, device_path):
    execute_adb_command(["-s", device_id, "install", device_path])

# Integration
#apk_path = download_latest_apk("repo_url")
#device_path = copy_apk_to_device("device_id", apk_path)
#install_apk_on_device("device_id", device_path)