# 1. Présentation du sujet 

Ce projet consiste en le développement et le déploiement d'une API Python (FastAPI) conteneurisée avec Docker, visant à automatiser la gestion de données sur Google Cloud Storage et la génération de contenu créatif via les modèles de langage de Vertex AI.

# 2. Exécution en local :

- python -m venv venv

venv\Scripts\activate

- python -m pip install --upgrade pip

pip install fastapi uvicorn

- cd api

python -m uvicorn app.main:app --reload

- Lancer : 

http://127.0.0.1:8000/docs#/default/post_data_data_post

# 3. Build et Run avec Docker :

- docker build -t mini-api-image .

docker run -p 8080:8080 mini-api-image

docker tag mini-api-image emmandlc/mini-api-esme:latest

docker push emmandlc/mini-api-esme:latest

Lancer : http://localhost:8080/docs#/default

- docker build -t leonies29/hands-on:latest .

docker push leonies29/hands-on:latest

# 4. Déploiement Cloud :

- Build et push de l'image via Cloud Build
- Déploiement sur Cloud Run avec les variables d'environnement configurées.
(Nous avons juste un problème avec /poem car nous n'arrivons pas à avoir accès à Vertex AI donc il renvoie un poème par défaut.)

# Lien Cloud Run :

https://mini-api-esme-366915979462.europe-west1.run.app/docs

# Lien Docker Hub : 

https://hub.docker.com/r/emmandlc/mini-api-esme

# Lien GitHub : 

https://github.com/Leonies29/projet-hands-on
