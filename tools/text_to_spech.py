import pyttsx3
import sys

def text_to_speech(text):
    """
    Énonce le texte fourni en utilisant le module pyttsx3.

    Args:
        text (str): Le texte à énoncer.
    """
    # Initialisation de pyttsx3
    engine = pyttsx3.init()

    # Configurer la voix (optionnel)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "fr_FR" in voice.id:
            engine.setProperty('voice', voice.id)

    # Configurer le débit de parole (optionnel)
    engine.setProperty('rate', 150)  # Ajuste la vitesse de lecture (valeur par défaut ~200)

    # Énoncer le texte
    engine.say(text)
    engine.runAndWait()

# Exemple d'utilisation
if __name__ == "__main__":
    text_to_speech(sys.argv[1])