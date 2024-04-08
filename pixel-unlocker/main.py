from utils.adb_utils import setup_adb
from modules.device_checker import get_connected_devices, get_device_model
from modules.bootloader import unlock_bootloader, wait_for_device_bootloader

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
        model = get_device_model(device_id)
        if "Pixel" in model:
            print(f"Pixel device detected: {device_id}, Model: {model}")
            user_response = input(f"Do you want to unlock the bootloader of {model}? (y/n): ").lower()
            if user_response == 'y':
                unlock_bootloader(device_id, model)
                if wait_for_device_bootloader(device_id):
                    reboot_device(device_id)
            else:
                print(f"Skipping bootloader unlock for {device_id}. ({model})")
        else:
            print(f"Non-Pixel device detected: {device_id}, skipping.")

if __name__ == "__main__":
    main()

