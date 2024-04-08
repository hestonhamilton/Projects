#!/usr/bin/env python3
from utils.adb_utils import execute_adb_command

def get_connected_devices():
    _, stdout, _ = execute_adb_command(["devices"])
    devices = []
    for line in stdout.splitlines():
        if "\tdevice" in line:
            device_id = line.split("\t")[0]
            devices.append(device_id)
    return devices

def is_pixel_device(device_id):
    command = ["shell", "getprop", "ro.product.model"]
    _, model, _ = execute_adb_command(["-s", device_id] + command)
    return "Pixel" in model