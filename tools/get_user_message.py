import speech_recognition as sr


def get_user_message():
    """
    Get user message
    :return: str | None
    """
    # Initialiser le reconnaisseur
    recognizer = sr.Recognizer()

    # Utiliser le microphone comme source d'audio
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        # Ajuster l'énergie du bruit ambiant
        recognizer.adjust_for_ambient_noise(source)
        # Capturer l'audio
        audio = recognizer.listen(source)

        try:
            # Reconnaître la parole en utilisant Google Web Speech API
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris."
        except sr.RequestError as e:
            print("Erreur du service de reconnaissance vocale ; {0}".format(e))
            return None
