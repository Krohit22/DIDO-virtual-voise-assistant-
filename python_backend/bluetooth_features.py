

import pyautogui
import subprocess

import time
import subprocess

def is_bluetooth_on():
    try:
        # PowerShell command to get Bluetooth devices with 'OK' status
        cmd = 'powershell.exe "Get-PnpDevice -Class Bluetooth | Select-Object Status"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            print(" Error: PowerShell command failed.")
            print(result.stderr)
            return False

        # Process output
        statuses = result.stdout.strip().split("\n")[2:]  # Skip headers

        # Debugging: Print all statuses
        print(" Bluetooth Device Statuses:", statuses)

        # Check if any status is 'Unknown'
        for status in statuses:
            if "Unknown" in status:
                print(" Found 'Unknown' status. Bluetooth might be off.")
                return False

        print(" Bluetooth is ON (No 'Unknown' status found).")
        return True

    except Exception as e:
        print(f" Exception: {e}")
        return False

# Example Usage
bluetooth_status = is_bluetooth_on()
print("Bluetooth ON:", bluetooth_status)


def bluetooth_on_and_off():
    pyautogui.hotkey('win', 'a')  # Open Action Center
    time.sleep(1)  # Wait for it to open

    pyautogui.press('right')  # Move to the Bluetooth toggle
    time.sleep(0.2)

    pyautogui.press('enter')  # Toggle Bluetooth
    time.sleep(1)

    pyautogui.hotkey('win', 'a')  # Close Action Center

print(is_bluetooth_on())
