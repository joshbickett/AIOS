import subprocess
import os
from datetime import datetime


def take_snippet_and_save():
    # Ensure the path is absolute

    save_path = get_save_path()

    path = os.path.abspath(save_path)

    # Use macOS's screencapture utility for interactive capture
    subprocess.run(["screencapture", "-i", path])

    # Check if the file was created since screencapture does not capture if the user cancels
    if os.path.isfile(path):
        print(f"Snippet saved to {path}")
    else:
        print("Snippet capture cancelled or failed.")


def get_save_path():
    # Define the folder name
    folder_name = "screenshots"

    # Get the current directory of the Python script
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create the full path for the screenshots directory
    screenshots_directory = os.path.join(current_directory, folder_name)

    # Check if the directory exists, if not, create it
    if not os.path.exists(screenshots_directory):
        os.makedirs(screenshots_directory)

    # Create a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define the filename with the timestamp
    filename = f"screenshot_{timestamp}.png"

    # Create the full save path
    save_path = os.path.join(screenshots_directory, filename)

    return save_path
