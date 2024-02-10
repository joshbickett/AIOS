import subprocess


def ask_user_input():
    try:
        # AppleScript for input dialog
        script = """display dialog "Enter your message:" default answer ""
        """
        # Run the AppleScript
        proc = subprocess.run(
            ["osascript", "-e", script], text=True, capture_output=True
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
        else:
            print("Error: Failed to execute AppleScript.")
            return None
    except subprocess.SubprocessError as e:
        print(f"An error occurred: {e}")
        return None
