import subprocess
import os
from datetime import datetime
import base64
from config import Config

verbose = Config().verbose


def take_snippet_and_save():
    save_path = get_save_path()
    path = os.path.abspath(save_path)

    # Use macOS's screencapture utility for interactive capture
    subprocess.run(["screencapture", "-i", path])

    # Convert the image to base64 if it exists
    if os.path.isfile(path):
        if verbose:
            print(f"Snippet saved to {path}")
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string  # Return the base64 string
    else:
        print("Snippet capture cancelled or failed.")
        return None


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


def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string
