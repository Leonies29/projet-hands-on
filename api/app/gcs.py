import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOCAL_PATH = DATA_DIR / "store.json"


def _default_store() -> Dict[str, Any]:
    return {"rows": []}


def _load_local() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOCAL_PATH.is_file():
        data = _default_store()
        LOCAL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    return json.loads(LOCAL_PATH.read_text(encoding="utf-8"))


def _save_local(data: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _bucket_name() -> Optional[str]:
    name = os.getenv("GCS_BUCKET", "").strip()
    return name or None


def _object_path() -> str:
    return os.getenv("GCS_OBJECT_PATH", "data/store.json").strip() or "data/store.json"


def read_data() -> Dict[str, Any]:
    bucket = _bucket_name()
    if not bucket:
        return _load_local()
    from google.cloud import storage

    client = storage.Client()
    b = client.bucket(bucket)
    blob = b.blob(_object_path())
    if not blob.exists():
        return _default_store()
    raw = blob.download_as_text(encoding="utf-8")
    return json.loads(raw)


def write_data(data: Dict[str, Any]) -> None:
    bucket = _bucket_name()
    if not bucket:
        _save_local(data)
        return
    from google.cloud import storage

    client = storage.Client()
    b = client.bucket(bucket)
    blob = b.blob(_object_path())
    blob.upload_from_string(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type="application/json; charset=utf-8",
    )
