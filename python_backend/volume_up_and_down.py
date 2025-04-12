import pythoncom  # Import this to initialize COM
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from Speak_func import speak  # Ensure this function exists

def change_volume(percent_change):
    """
    Adjusts the system volume by a given percentage.
    :param percent_change: Positive to increase, negative to decrease.
    """
    try:
        pythoncom.CoInitialize()  # Ensure COM is initialized

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Get the current volume level (0.0 to 1.0)
        current_volume = volume.GetMasterVolumeLevelScalar()

        # Calculate new volume
        new_volume = max(0.0, min(1.0, current_volume + (percent_change / 100)))

        # Set new volume
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak(f"Volume set to {int(new_volume * 100)}%")

    except Exception as e:
        print(f"Error adjusting volume: {e}")

def current_volume():
    """
    Returns the current system volume as a percentage.
    """
    try:
        pythoncom.CoInitialize()  # Ensure COM is initialized

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Get the current volume level (0.0 to 1.0)
        return int(volume.GetMasterVolumeLevelScalar() * 100)

    except Exception as e:
        print(f"Error fetching volume: {e}")
        return None  # Handle error gracefully



