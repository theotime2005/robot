import sys
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar
import tools

PROMPT_DESCRIPTION = "Tu fais de l'audio description pour une personne non voyante. Voici une photo. Décris-la aussi précisément que possible."

class RobotWorker(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # Start with taking picture
            self.update_signal.emit("image")
            image = tools.capture_photo_to_tmp()

            # Continue with analyzing picture
            self.update_signal.emit("gemini")
            analyseur = tools.AnalyseurImageGemini(image)
            analyseur.telecharger_image()
            response = analyseur.description(PROMPT_DESCRIPTION)
            if not response:
                self.update_signal.emit("error")
                return

            # End with say response.
            self.update_signal.emit("saying")
            tools.text_to_speech(response)
            self.update_signal.emit("success")
        except Exception as e:
            print(e)
            self.update_signal.emit("error")

class RobotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot")
        self.setGeometry(100, 100, 300, 200)

        # Layout
        self.layout = QVBoxLayout()

        # Titre
        self.title_label = QLabel("Bienvenue dans l'application Robot")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Bouton
        self.start_button = QPushButton("Lancer l'analyse")
        self.start_button.clicked.connect(self.start_analysis)
        self.layout.addWidget(self.start_button)

        # Label de statut
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Indicateur de chargement
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Pour un indicateur de chargement sans valeur précise
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def start_analysis(self):
        # Désactive le bouton pendant l'analyse
        self.start_button.setEnabled(False)

        # Démarrer le processus de l'analyse dans un thread séparé
        self.worker = RobotWorker()
        self.worker.update_signal.connect(self.update_status)
        self.worker.start()

    def update_status(self, status):
        if status == "image":
            self.progress_bar.setVisible(True)
            self.status_label.setText("Nous prenons la photo")
        elif status == "gemini":
            self.status_label.setText("Nous analysons l'image")
        elif status == "saying":
            self.status_label.setText("Énonciation")
        elif status == "success":
            self.status_label.setText("")
            self.progress_bar.setVisible(False)
            self.start_button.setEnabled(True)
        elif status == "error":
            self.status_label.setText("Une erreur est survenue")
            self.progress_bar.setVisible(False)
            self.start_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotApp()
    window.show()
    sys.exit(app.exec())
