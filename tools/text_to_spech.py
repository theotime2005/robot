import sys
from gtts import gTTS
from playsound import playsound
import tempfile

def text_to_speech(text):
    """
    Énonce le texte en utilisant gTTS et playsound.
    """
    tts = gTTS(text, lang="fr")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        playsound(tmp_file.name)


# Exemple d'utilisation
if __name__ == "__main__":
    text_to_speech(sys.argv[1])