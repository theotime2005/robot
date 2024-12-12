# seeHead  

## Objectif d’automatisation  
Une tête de robot pivotante dotée d'une caméra capable de décrire l'environnement.

---

## ODD (Operational Domain Design)  
Ajoutez ici votre diagramme de conception opérationnelle (ODD) et décrivez les valeurs limites.  
- Exemple :  
  ![Diagramme ODD](url_du_diagramme)  
  - Valeur limite 1 : …  
  - Valeur limite 2 : …  

---

## Schéma d'architecture logique et physique  
Incluez vos schémas en expliquant le rôle de chaque composant.  
- Exemple :  
  - Architecture logique : ![Schéma logique](url_du_schéma_logique)  
  - Architecture physique : ![Schéma physique](url_du_schéma_physique)  

---

## Schéma électronique  
Ajoutez ici un schéma clair des composants électroniques et des connexions.  
- Exemple : ![Schéma électronique](url_du_schéma_électronique)  

---

## Fichiers de testes
A compléter.

---

## Instructions de déploiement   
1. Clonez ce dépôt :  
   ```bash
   git clone https://github.com/theotime2005/robot
   cd robot
   ```
2. Mettre en place le projet  
   ```bash
   sh setup.sh
   ```
   3. Lancez le projet
   1. Via l'interface graphique sur ordinateur
    ```bash
   python interface.py
   ```
   2. Via le fichier main pour un rendu en ligne de commande
   ```bash
   python main.py
   ```
   Vous pouvez alors appuyer sur o pour utiliser Ollama et g pour Gemini.

Note: Vous devez installer Ollama pour utiliser la partie ollama. Sinon, vous devrez utiliser Gemini. Vous pouvez créer une clef API pour Gemini gratuitement.

---

## Dépendances**
- wheel
- google-generativeai
- gtts
- ollama
- opencv-python
- playsound
- PyObjC
- python-dotenv
- pyqt6

---
