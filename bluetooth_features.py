import wmi

import subprocess
import os
def get_bluetooth_hardware_id():
    c = wmi.WMI()
    for device in c.Win32_PnPEntity():
        if "bluetooth" in str(device.Name).lower():
            print(f"Device: {device.Name}")
            print(f"Hardware ID: {device.PNPDeviceID}\n")
            return device.PNPDeviceID

    print("No Bluetooth device found.")
    return None

BLUETOOTH_HARDWARE_ID = get_bluetooth_hardware_id()
print(f"BLUETOOTH_HARDWARE_ID = \"{BLUETOOTH_HARDWARE_ID}\"")




def bluetooth_off():
    subprocess.run(f"devcon disable \"{BLUETOOTH_HARDWARE_ID}\"", shell=True)
    print("Bluetooth Disabled")

def bluetooth_on():
    subprocess.run(f"devcon enable \"{BLUETOOTH_HARDWARE_ID}\"", shell=True)
    print("Bluetooth Enabled")

# Example Usage
bluetooth_off()
