from pynput import keyboard
import time
from utils import take_snippet_and_save
from gui import ask_user_input


class DoubleCmdListener:
    def __init__(self):
        self.cmd_pressed = False
        self.last_cmd_time = 0
        self.time_threshold = 0.2  # Time threshold in seconds for double press
        self.last_key = None

    def on_press(self, key):
        current_time = time.time()
        if key == keyboard.Key.cmd:
            print("cmd pressed")
            if (
                self.cmd_pressed
                and current_time - self.last_cmd_time <= self.time_threshold
                and key
                == self.last_key  # Check if the last key is the same as the current key
            ):
                print("DOUBLE 'Cmd' pressed!")
                take_snippet_and_save()
                # Add the call to the ask_user_input
                message = ask_user_input()
                print("User entered:", message)
                self.cmd_pressed = False  # Reset after detection
            else:
                self.cmd_pressed = True
                self.last_cmd_time = current_time
                self.last_key = key  # Save the last key pressed
        else:
            print("reset because key press: ", key)
            self.cmd_pressed = False  # Reset if any other key is pressed

    def on_release(self, key):
        pass


def main():
    listener = DoubleCmdListener()
    with keyboard.Listener(
        on_press=listener.on_press, on_release=listener.on_release
    ) as l:
        l.join()


if __name__ == "__main__":
    main()
