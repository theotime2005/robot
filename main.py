from pynput import keyboard

from robot import Robot
from tools.text_to_speech import text_to_speech


class RobotMain:
    def __init__(self):
        self.robot = None
        # Initialize keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            # Convert char to uppercase and check the key pressed
            press_key = key.char.upper()
            if press_key == "G" and not self.robot:
                self._start_robot("gemini")
            elif press_key == "O" and not self.robot:
                self._start_robot("ollama")
        except AttributeError:
            # Handle special keys (e.g., Shift, Ctrl) that don't have a 'char' attribute
            pass
        except Exception as e:
            print(f"Erreur: {e}")

    def on_release(self, key):
        # No action on key release for now
        pass

    def _start_robot(self, model_name):
        """Start the robot with the specified model."""
        self.robot = Robot(
            model=model_name,
            function_on_progress=self._progress,
            function_on_end=self._end
        )
        self.robot.start()

    def _progress(self, message):
        """Handle progress messages from the robot."""
        if message == "image":
            text_to_speech("Je prends la photo")
        elif message == "analyse":
            text_to_speech("J'analyse l'image")
        else:
            # Handle unexpected progress messages gracefully
            print(f"Progress: {message}")

    def _end(self, message, time):
        """Handle end messages from the robot."""
        if message == "error":
            text_to_speech("Il y a une erreur")
        else:
            print(f"Execution completed in {time} seconds.")
        self.robot = None


# Start
if __name__ == "__main__":
    robot_main = RobotMain()
    robot_main.listener.join()
