import sys

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QComboBox

import tools
from tools.timer import TimerExecution


class RobotWorker(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        try:
            # Start with taking picture
            self.update_signal.emit("image")
            image = tools.capture_photo_to_tmp()

            # Continue with analyzing picture
            self.update_signal.emit("analyse")
            if self.model == "gemini":
                analyseur = tools.AnalyseurImageGemini(image)
                analyseur.telecharger_image()
                response = analyseur.description()
                if not response:
                    self.update_signal.emit("error")
                    return
            elif self.model == "ollama":
                analyseur = tools.AnalyseurOllama(image)
                response = analyseur.send_question()
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
        self.timer = TimerExecution()
        super().__init__()
        self.setWindowTitle("Robot")
        self.setGeometry(100, 100, 300, 200)

        # Layout
        self.layout = QVBoxLayout()

        # Titre
        self.title_label = QLabel("Bienvenue dans l'application Robot")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Dropdown menu
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItems(["gemini", "ollama"])
        self.layout.addWidget(self.dropdown_menu)

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
        self.dropdown_menu.setEnabled(False)

        # Récupère la sélection du menu déroulant
        selected_option = self.dropdown_menu.currentText()

        # Démarrer le processus de l'analyse dans un thread séparé
        self.worker = RobotWorker(selected_option)
        self.worker.update_signal.connect(self.update_status)
        self.timer.start_timer()
        self.worker.start()

    def update_status(self, status):
        if status == "image":
            self.progress_bar.setVisible(True)
            self.status_label.setText("Nous prenons la photo")
        elif status == "analyse":
            self.status_label.setText("Nous analysons l'image")
        elif status == "saying":
            self.status_label.setText("Énonciation")
        elif status == "success":
            self.timer.stop_timer()
            self.progress_bar.setVisible(False)
            self.status_label.setText(f"Réalisé en {self.timer.result}")
            self.start_button.setEnabled(True)
            self.dropdown_menu.setEnabled(True)
        elif status == "error":
            self.timer.stop_timer()
            self.status_label.setText(f"Une erreur est survenue après {self.timer.result}")
            self.progress_bar.setVisible(False)
            self.start_button.setEnabled(True)
            self.dropdown_menu.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotApp()
    window.show()
    sys.exit(app.exec())
