from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
 
from app.gcs import read_data, write_data
from app.vertex import generate_poem
 
app = FastAPI(title="Mini API", version="1.0.0")

@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur notre API !"}

@app.get("/status")
def status():
    return {"server_time_utc": datetime.now(timezone.utc).isoformat()}
  
@app.get("/poem")
def get_poem():
    if os.getenv("GCP_PROJECT", "").strip():
        try:
            return {"poem": _poem_vertex()}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Vertex error: {e}") from e

@app.get("/data")
def get_data():
    data = _load_store()
    if "rows" not in data:
        data = {"rows": []}
    return data

@app.post("/data")
def post_data(body: LineBody):
    text = (body.line or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail='Champ "line" requis et non vide.')
 
    data = _load_store()
    rows = list(data.get("rows", []))
    rows.append(text)
    out = {"rows": rows}
    _save_store(out)
    return {"ok": True, "rows": rows}