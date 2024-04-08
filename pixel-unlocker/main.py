from utils.adb_utils import setup_adb
from modules.device_checker import get_connected_devices, is_pixel_device
from modules.bootloader import unlock_bootloader

def main():
    # Setup ADB; this will install it in the project directory if not present in the system
    adb_path = setup_adb()
    if not adb_path:
        print("Failed to set up ADB. Exiting.")
        return

    devices = get_connected_devices()

    if not devices:
        print("No device connected.")
        return

    for device_id in devices:
        if is_pixel_device(device_id):
            print(f"Pixel device detected: {device_id}")
            user_response = input("Do you want to unlock the bootloader? (y/n): ").lower()
            if user_response == 'y':
                unlock_bootloader(device_id)
            else:
                print(f"Skipping bootloader unlock for {device_id}.")
        else:
            print(f"Non-Pixel device detected: {device_id}, skipping.")

if __name__ == "__main__":
    main()

