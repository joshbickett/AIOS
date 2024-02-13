from pynput import keyboard
import time
from utils import take_snippet_and_save
from gui import ask_user_input

from apis import call_openai
from prompts import get_system_prompt
from config import Config

verbose = Config().verbose


class AIOS:
    def __init__(self, messages):
        self.cmd_pressed = False
        self.app_active = False
        self.last_cmd_time = 0
        self.time_threshold = 0.2  # Time threshold in seconds for double press
        self.last_key = None
        self.messages = messages  # Store messages as an instance attribute

    def on_press(self, key):
        current_time = time.time()
        if key == keyboard.Key.cmd:
            if verbose:
                print("[on_press] cmd pressed")
            if (
                self.cmd_pressed
                and current_time - self.last_cmd_time <= self.time_threshold
            ):
                if not self.app_active:
                    self.app_active = True
                    # Code to activate the app
                    img_base64 = take_snippet_and_save()
                    if img_base64:
                        user_message = ask_user_input()
                        print("[user]", user_message)
                        call_openai(self.messages, user_message, img_base64)
                        self.cmd_pressed = False
                        self.app_active = (
                            False  # Add this line if you also need to reset app_active
                        )
                self.cmd_pressed = False
            else:
                self.cmd_pressed = True
                self.last_cmd_time = current_time
                self.last_key = key
        elif self.app_active:
            # Handle other keys when app is active
            if verbose:
                print(f"[on_press] {key}")
            # Add condition to reset self.app_active if needed
        else:
            self.cmd_pressed = False  # Reset if any other key is pressed
            if verbose:
                print(f"[on_press] {key}")

    def on_release(self, key):
        pass


def main():
    system_message = get_system_prompt()
    messages = [
        {"role": "system", "content": system_message},
    ]
    listener = AIOS(messages)  # Pass messages to the listener
    with keyboard.Listener(
        on_press=listener.on_press, on_release=listener.on_release
    ) as l:
        l.join()


if __name__ == "__main__":
    main()
