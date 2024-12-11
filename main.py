# Point d'entré pour le processus du robot
# On va utiliser la configuration pour ordinateur
# Ce fichier sera appelé depuis l'interface graphique.
import threading
import tools as tools
from timer import TimerExecution

PROMPT_DESCRIPTION = "Tu fais de l'audio description pour une personne non voyante. Voici une photo. Décris-la aussi précisément que possible."

class Robot(threading.Thread):
    def __init__(self, function_on_progress, function_on_end):
        self.timer = TimerExecution()
        threading.Thread.__init__(self)
        self.function_on_progress = function_on_progress
        self.function_on_end = function_on_end

    def run(self):
        self.timer.start_timer()
        try:
            # Start with take picture
            self.function_on_progress("image")
            image = tools.capture_photo_to_tmp()
            # Continue with analyzing picture
            self.function_on_progress("gemini")
            analyseur = tools.AnalyseurImageGemini(image)
            analyseur.telecharger_image()
            response = analyseur.description(PROMPT_DESCRIPTION)
            if not response:
                return self.__end("error")
            # End with say response.
            self.function_on_progress("saying")
            tools.text_to_speech(response)
            self.__end("success")
        except Exception as e:
            print(e)
            self.__end("error")

    def __end(self, message):
        self.timer.stop_timer()
        self.function_on_end(message, self.timer.result)

# Test du lanceur
if __name__ == "__main__":
    robot = Robot(print, print)
    robot.start()
    robot.join()  # Attend que le thread se termine avant de quitter le programme
