from pynput import keyboard
import time
from utils import take_snippet_and_save
from gui import ask_user_input

from apis import call_openai
from prompts import get_system_prompt


class AIOS:
    def __init__(self, messages):
        self.cmd_pressed = False
        self.last_cmd_time = 0
        self.time_threshold = 0.2  # Time threshold in seconds for double press
        self.last_key = None
        self.messages = messages  # Store messages as an instance attribute

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
                img_base64 = take_snippet_and_save()
                if img_base64:
                    user_prompt = ask_user_input()
                    call_openai(
                        self.messages, user_prompt, img_base64
                    )  # Pass img_base64 here

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
