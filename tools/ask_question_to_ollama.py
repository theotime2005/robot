import os
import sys

from ollama import Client
from dotenv import load_dotenv, find_dotenv

# Charger les variables d'environnement
load_dotenv(find_dotenv())
API_URL = os.getenv("OLLAMA_URL")

PROMPT_FILE_NAME = "prompt.txt"
folder_path = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE_PATH = os.path.join(folder_path, PROMPT_FILE_NAME)


class AnalyseurOllama:
    def __init__(self, image_path):
        self.image_path = image_path
        self.prompt = ""
        self.import_prompt()

    def import_prompt(self):
        try:
            with open(PROMPT_FILE_PATH, "r") as file:
                self.prompt = file.read()
            return True
        except Exception as e:
            return False

    def send_question(self):
        if not self.image_path:
            return False
        client = Client(
            host=API_URL, headers={"x-some-header": "some-value"}
        )
        response = client.chat(
            model="llama3.2-vision",
            messages=[
                {"role": "user", "content": self.prompt, "images": [self.image_path]},
            ],
        )
        return response.message.content


if __name__ == "__main__":
    from timer import TimerExecution

    timer = TimerExecution()
    image_path = sys.argv[1]
    timer.start_timer()
    analyseur = AnalyseurOllama(image_path)
    if not analyseur.import_prompt():
        timer.stop_timer()
        print("Erreur lors de l'importation du prompt.")
        sys.exit(1)
    response = analyseur.send_question()
    timer.stop_timer()
    if response:
        print(f"Réponse: {response}")
        print(f"Temps d'exécution: {timer.result}")
    else:
        print("Erreur aucune réponse obtenues.")
