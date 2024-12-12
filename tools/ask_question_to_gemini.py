import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Charger les variables d'environnement
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

# Vérifier si la clé API est présente
if not api_key:
    raise ValueError("La clé API GEMINI_API_KEY n'est pas définie dans les variables d'environnement.")

# Configurer l'API Gemini
genai.configure(api_key=api_key)

PROMPT_FILE_NAME = "prompt.txt"
folder_path = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE_PATH = os.path.join(folder_path, PROMPT_FILE_NAME)

class AnalyseurImageGemini:
    def __init__(self, chemin_image):
        """
        Initialise l'analyseur avec le chemin de l'image à analyser.
        :param chemin_image: Chemin vers l'image à analyser
        """
        self.prompt = ""
        self.chemin_image = chemin_image
        self.fichier = None
        self.load_prompt()

    def telecharger_image(self):
        """
        Télécharge l'image vers l'API Gemini et stocke l'objet File résultant.
        """
        try:
            self.fichier = genai.upload_file(self.chemin_image, mime_type="image/jpeg")
            return True
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image : {e}")
            return False

    def load_prompt(self):
        try:
            with open(PROMPT_FILE_PATH, "r") as file:
                self.prompt = file.read()
        except Exception as e:
            return False

    def description(self):
        """
        Décrire l'image
        :return: str
        """
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([self.fichier, self.prompt])
        return response.text

# Exemple d'utilisation
if __name__ == "__main__":
    from timer import TimerExecution
    timer = TimerExecution()
    chemin_image = sys.argv[1]
    timer.start_timer()

    analyseur = AnalyseurImageGemini(chemin_image)
    analyseur.telecharger_image()
    response = analyseur.description()
    timer.stop_timer()
    if response:
        print(f"Réponse: {response}")
        print(f"Temps d'exécution: {timer.result}")
    else:
        print("Erreur aucune réponse obtenues.")