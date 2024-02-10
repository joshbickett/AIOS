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
            # Parse the output to extract user input
            output_lines = proc.stdout.strip().split(
                ":"
            )  # Split at ":" to separate button and text returned
            user_input = output_lines[
                -1
            ].strip()  # Last part contains the text returned
            return user_input
        else:
            print("Error: Failed to execute AppleScript.")
            return None
    except subprocess.SubprocessError as e:
        print(f"An error occurred: {e}")
        return None
