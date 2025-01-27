import math
import time
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pyttsx3

# Set the default volume value
DEFAULT_VOLUME = 0.25  # Volume value between 0.0 and 1.0

# Initialize the text-to-speech engine once
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Activate the audio interface once
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))


# Function to read the current volume
def get_current_volume(volume_control):
    return volume_control.GetMasterVolumeLevelScalar()


# Function to set the volume
def set_volume(volume, volume_control):
    volume_control.SetMasterVolumeLevelScalar(volume, None)
    print(f"Volume set to: {volume * 100:.0f}%")


# Main logic
try:
    set_volume(DEFAULT_VOLUME, volume_control)

    while True:
        time.sleep(3)
        current_volume = get_current_volume(volume_control)

        print(f"Current volume: {current_volume * 100:.0f}%")

        if math.fabs(current_volume - DEFAULT_VOLUME) * 100 >= 1:
            print(
                f"Current volume ({current_volume * 100:.0f}%) is different from default ({DEFAULT_VOLUME * 100:.0f}%).")
            time.sleep(1)
            set_volume(DEFAULT_VOLUME, volume_control)
            text_to_speak = "order received"

            # Speak the text
            engine.say(text_to_speak)

            # Wait until the speaking is finished
            engine.runAndWait()
        else:
            print("Current volume is already at the default value.")
finally:
    # Clean up resources
    print('bye')
    engine.stop()
    del volume_control  # Explicitly delete the COM object reference
