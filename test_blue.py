"""from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Set the default volume value
DEFAULT_VOLUME = 0.5  # Volume value between 0.0 and 1.0

# Function to read the current volume
def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()

# Function to set the volume
def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
    volume_control.SetMasterVolumeLevelScalar(volume, None)
    print(f"Volume set to: {volume * 100:.0f}%")

# Main logic
current_volume = get_current_volume()

print(f"Current volume: {current_volume * 100:.0f}%")

if current_volume != DEFAULT_VOLUME:
    print(f"Current volume ({current_volume * 100:.0f}%) is different from default ({DEFAULT_VOLUME * 100:.0f}%).")
    set_volume(DEFAULT_VOLUME)
else:
    print("Current volume is already at the default value.")"""

import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)

# Text to be spoken
text_to_speak = "Checkmate, white won"

# Speak the text
engine.say(text_to_speak)

# Wait until the speaking is finished
engine.runAndWait()