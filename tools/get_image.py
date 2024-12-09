import cv2
import os
import tempfile

def capture_photo_to_tmp():
    """
    Capture une photo depuis la webcam et la stocke dans le dossier temporaire du système.
    Retourne le chemin complet du fichier enregistré.
    """
    # Initialiser la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Impossible d'accéder à la webcam.")

    # Lire une image
    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise Exception("Impossible de capturer une image depuis la webcam.")

    # Générer un chemin de fichier temporaire
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, "photo_captured.jpg")

    # Sauvegarder l'image
    cv2.imwrite(file_path, frame)

    # Libérer la webcam
    cap.release()
    cv2.destroyAllWindows()

    return file_path

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        photo_path = capture_photo_to_tmp()
        print(f"Photo capturée et enregistrée ici : {photo_path}")
    except Exception as e:
        print(f"Erreur : {e}")
