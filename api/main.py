"""
API mini-projet : routes obligatoires + GCS / Vertex derrière variables d’environnement.
Sans GCS_BUCKET → lecture/écriture locale (api/data/store.json) pour avancer tout de suite.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_DIR = Path(__file__).resolve().parent / "data"
LOCAL_PATH = DATA_DIR / "store.json"


class LineBody(BaseModel):
    line: str


app = FastAPI(title="Mini-projet API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _default_store() -> dict:
    return {"rows": []}


def _load_local() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOCAL_PATH.is_file():
        data = _default_store()
        LOCAL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    return json.loads(LOCAL_PATH.read_text(encoding="utf-8"))


def _save_local(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _gcs_bucket_name() -> Optional[str]:
    name = os.getenv("GCS_BUCKET", "").strip()
    return name or None


def _gcs_object_path() -> str:
    return os.getenv("GCS_OBJECT_PATH", "data/store.json").strip() or "data/store.json"


def _load_store() -> dict:
    bucket = _gcs_bucket_name()
    if not bucket:
        return _load_local()
    try:
        from google.cloud import storage

        client = storage.Client()
        b = client.bucket(bucket)
        blob = b.blob(_gcs_object_path())
        if not blob.exists():
            return _default_store()
        raw = blob.download_as_text(encoding="utf-8")
        return json.loads(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCS read error: {e}") from e


def _save_store(data: dict) -> None:
    bucket = _gcs_bucket_name()
    if not bucket:
        _save_local(data)
        return
    try:
        from google.cloud import storage

        client = storage.Client()
        b = client.bucket(bucket)
        blob = b.blob(_gcs_object_path())
        blob.upload_from_string(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type="application/json; charset=utf-8",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCS write error: {e}") from e


def _poem_vertex() -> str:
    project = os.getenv("GCP_PROJECT", "").strip()
    location = os.getenv("VERTEX_LOCATION", "europe-west1").strip()
    if not project:
        raise HTTPException(
            status_code=503,
            detail="Vertex désactivé : définir GCP_PROJECT (et credentials GCP).",
        )
    import vertexai
    from vertexai.generative_models import GenerativeModel

    vertexai.init(project=project, location=location)
    model = GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(
        "Écris un très court poème en français (4 vers), thème : nuages et code."
    )
    text = (resp.text or "").strip()
    if not text:
        raise HTTPException(status_code=502, detail="Vertex a renvoyé une réponse vide.")
    return text


@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur l'API du mini-projet."}


@app.get("/status")
def status():
    return {"server_time_utc": datetime.now(timezone.utc).isoformat()}


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


@app.get("/poem")
def get_poem():
    """
    Si GCP_PROJECT est défini et les credentials Vertex OK → poème via Vertex.
    Sinon → poème statique (pour tester le front sans GCP).
    """
    if os.getenv("GCP_PROJECT", "").strip():
        try:
            return {"poem": _poem_vertex()}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Vertex error: {e}") from e

    return {
        "poem": (
            "Sans Vertex pour l’instant :\n"
            "Un poème court en attendant le nuage,\n"
            "Ajoute GCP_PROJECT et tes credentials pour la suite."
        )
    }
