from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.gcs import read_data, write_data
from app.vertex import generate_poem

app = FastAPI(title="Mini API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LineBody(BaseModel):
    line: str


@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur notre API !"}


@app.get("/status")
def status():
    return {"server_time_utc": datetime.now(timezone.utc).isoformat()}


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


@app.get("/poem")
def get_poem():
    try:
        poem = generate_poem()
        return {"poem": poem}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
