from fastapi import FastAPI

# 1. On crée l'instance de l'application
app = FastAPI()

# 2. On définit l'endpoint GET /hello
@app.get("/hello")
def read_hello():
    return {
        "message": "Bonjour ! Bienvenue sur l'API de notre mini-projet en Data Science Tools.",
        "equipe": "Clara, Léonie et Emma",
        "status": "Success"
    }

# Ce bloc permet de lancer l'application directement avec 'python main.py'
if __name__ == "__main__":
    import uvicorn
    # Le port 8080 est celui exigé par Google Cloud Run
    uvicorn.run(app, host="0.0.0.0", port=8080)




@app.get("/status")
def status():
    return {
        "status": "ok",
        "datetime": datetime.now().isoformat()
    }