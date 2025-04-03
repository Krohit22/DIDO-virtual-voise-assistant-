import psutil
import time
from Speak_func import speak
def get_battery_status():
    """
    Retrieves the current battery status and percentage.
    :return: A tuple containing the battery percentage and charging status.
    """
    battery = psutil.sensors_battery()
    percent = battery.percent
    if battery.power_plugged and percent>50:
        speak(f"Your battery is at {percent} percent and is currently plug-in")
    elif battery.power_plugged and percent == 100:
        speak(f"Your battery is at {percent} percent and is fully charged and is currently plug-in so would you like to unplug it")
    elif not battery.power_plugged and percent > 50:
        speak(f"Your battery is at {percent} percent and is currently unplugged")
    elif not battery.power_plugged and percent < 50:
        speak(f"Your battery is at {percent} percent and is currently unplugged so please plug it in")
    elif percent < 15:
        speak(f"Your battery is at {percent} percent and is currently unplugged so it is critical please plug it in")
    elif not battery.power_plugged and percent == 100:
        speak(f"Your battery status is {percent} percent and is fully charged")

    
def is_plugged_in():

    battery = psutil.sensors_battery()
    return battery.power_plugged

