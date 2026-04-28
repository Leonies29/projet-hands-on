# 1. Présentation du sujet 

Ce projet consiste en le développement et le déploiement d'une API Python (FastAPI) conteneurisée avec Docker, visant à automatiser la gestion de données sur Google Cloud Storage et la génération de contenu créatif via les modèles de langage de Vertex AI.

# 2. Exécution en local :

- python -m venv venv

>> venv\Scripts\activate

- python -m pip install --upgrade pip

>> pip install fastapi uvicorn

- cd api

>> python -m uvicorn app.main:app --reload

- Lancer : 

http://127.0.0.1:8000/docs#/default/post_data_data_post

# 3. Build et Run avec Docker :

docker build -t mini-api .

# 4. Déploiement Cloud :

- Build de l'image via Cloud Build
- Déploiement sur Cloud Run avec les variables d'environnement configurées.