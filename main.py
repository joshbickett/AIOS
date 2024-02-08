from pynput import keyboard
import time


class DoubleCmdListener:
    def __init__(self):
        self.cmd_pressed = False
        self.last_cmd_time = 0
        self.time_threshold = 0.5  # Time threshold in seconds for double press

    def on_press(self, key):
        if key == keyboard.Key.cmd:  # Change to keyboard.Key.ctrl on Windows/Linux
            if (
                self.cmd_pressed
                and (time.time() - self.last_cmd_time) < self.time_threshold
            ):
                print("Double 'Cmd' pressed!")
                self.cmd_pressed = False  # Reset after detection
            else:
                self.cmd_pressed = True
                self.last_cmd_time = time.time()

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
