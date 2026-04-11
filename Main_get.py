from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
 
from app.gcs import read_data, write_data
from app.vertex import generate_poem
 
app = FastAPI(title="Mini API", version="1.0.0")

@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur notre API !"}