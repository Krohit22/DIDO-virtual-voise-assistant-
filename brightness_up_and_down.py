import screen_brightness_control as sbc
import pythoncom  # Import this to initialize COM
def change_brightness(percent_change):
    """
    Adjusts the screen brightness by a given percentage.
    :param percent_change: Positive to increase, negative to decrease.
    """
    pythoncom.CoInitialize()
    # Get current brightness level
    current_brightness = sbc.get_brightness()
    
    if isinstance(current_brightness, list):  
        current_brightness = current_brightness[0]  # Use first monitor

    # Calculate new brightness level
    new_brightness = current_brightness + percent_change
    new_brightness = max(0, min(100, new_brightness))  # Ensure between 0 and 100

    # Set new brightness
    sbc.set_brightness(new_brightness)
    print(f"💡 Brightness set to {new_brightness}%")

# Example Usage


