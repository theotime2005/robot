import sys
from gtts import gTTS
import tempfile
import subprocess

def text_to_speech(text, volume=400):
    """
    Énonce le texte en utilisant gTTS et VLC, avec un contrôle du volume.
    :param text: Le texte à énoncer.
    :param volume: Le volume (0 à 512 pour VLC).
    """
    gain = volume / 100
    tts = gTTS(text, lang="fr")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        # Utiliser VLC en ligne de commande pour lire le fichier audio avec volume ajusté
        subprocess.run([
            "vlc", "--intf", "dummy", "--play-and-exit", f"--gain={gain}", tmp_file.name
        ], check=True)

# Exemple d'utilisation
if __name__ == "__main__":
    if len(sys.argv) > 2:
        volume = int(sys.argv[2])  # Si un volume est fourni, on le récupère
    else:
        volume = 100  # Volume par défaut
    text_to_speech(sys.argv[1], volume)
