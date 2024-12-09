import os
import sys
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

# Vérifier si la clé API est présente
if not api_key:
    raise ValueError("La clé API GEMINI_API_KEY n'est pas définie dans les variables d'environnement.")

# Configurer l'API Gemini
genai.configure(api_key=api_key)



class AnalyseurImageGemini:
    def __init__(self, chemin_image):
        """
        Initialise l'analyseur avec le chemin de l'image à analyser.
        :param chemin_image: Chemin vers l'image à analyser
        """
        self.chemin_image = chemin_image
        self.fichier = None

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

    def description(self, prompt_text):
        """
        Décrire l'image
        :param prompt_text: str
        :return: str
        """
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([self.fichier, prompt_text])
        return response.text

# Exemple d'utilisation
if __name__ == "__main__":
    chemin_image = sys.argv[1]

    analyseur = AnalyseurImageGemini(chemin_image)
    analyseur.telecharger_image()
    response = analyseur.description("Décris cette image pour une personne aveugle.")
    if response:
        print(f"Réponse: {response}")
    else:
        print("Erreur aucune réponse obtenues.")