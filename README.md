1. Présentation du sujet 

Ce projet consiste en le développement et le déploiement d'une API Python (FastAPI) conteneurisée avec Docker, visant à automatiser la gestion de données sur Google Cloud Storage et la génération de contenu créatif via les modèles de langage de Vertex AI.

2. Exécution en local :

# Installation des dépendances
pip install -r api/requirements.txt
# Lancement
export BUCKET_NAME="votre-bucket"
export FILE_PATH="data.json"
uvicorn main:app --reload

3. Build et Run avec Docker :

docker build -t mini-api-image ./api
docker run -p 8080:8080 -e BUCKET_NAME="votre-bucket" mini-api-image

4. Déploiement Cloud :

--> Build de l'image via Cloud Build
--> Déploiement sur Cloud Run avec les variables d'environnement configurées.