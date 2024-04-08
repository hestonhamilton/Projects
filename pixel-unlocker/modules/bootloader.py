#!/usr/bin/env python3
from utils.adb_utils import execute_adb_command, execute_fastboot_command, reboot_device
import time
import subprocess

def wait_for_device_bootloader(device_id):
    timeout = 60  # Maximum time to wait (in seconds)
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            execute_adb_command(["fastboot", "-s", device_id, "getvar", "all"])
            return True  # Device is in bootloader mode
        except subprocess.CalledProcessError:
            time.sleep(2)  # Wait a bit before retrying

    return False  # Timeout reached

def unlock_bootloader(device_id):
    # Reboot device into bootloader mode
    execute_adb_command(["-s", device_id, "reboot", "bootloader"])

    # Wait for the device to reboot into bootloader mode
    if wait_for_device_bootloader(device_id):
        # Unlock the bootloader
        execute_fastboot_command(["-s", device_id, "flashing", "unlock"])
    
    # Reboot the device once it's done
    if wait_for_device_bootloader(device_id):
        reboot_device(device_id)

    print(f"Bootloader unlocked for device {device_id}")

def unlock_bootloader_pixel_7(device_id):
    # If Pixel 7 requires a specific procedure, implement it here,
    # otherwise, call the base method
    unlock_bootloader(device_id)

def unlock_bootloader_pixel_6(device_id):
    # If Pixel 6 requires a specific procedure, implement it here,
    # otherwise, call the base method    
    unlock_bootloader(device_id)