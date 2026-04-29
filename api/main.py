from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import os
 
from app.gcs import read_data, write_data
from app.vertex import generate_poem


class LineBody(BaseModel):
    line: str
 
app = FastAPI(title="Mini API", version="1.0.0")

@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur notre API !"}

@app.get("/status")
def status():
    return {"server_time_utc": datetime.now(timezone.utc).isoformat()}
  
@app.get("/poem")
def get_poem():
    try:
        return {"poem": generate_poem()}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Vertex error: {e}")

@app.get("/data")
def get_data():
    data = read_data()
    if "rows" not in data:
        data = {"rows": []}
    return data

@app.post("/data")
def post_data(body: LineBody):
    text = (body.line or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail='Champ "line" requis et non vide.')
 
    data = read_data()
    rows = list(data.get("rows", []))
    rows.append(text)
    out = {"rows": rows}
    write_data(out)
    return {"ok": True, "rows": rows}