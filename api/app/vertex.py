import os

def generate_poem() -> str:
    project = os.getenv("GCP_PROJECT", "").strip()
    if not project:
        return (
            "Le vent souffle sur les branches.\n"
            "La nuit tombe doucement.\n"
            "Les étoiles veillent là-haut.\n"
            "Demain sera un autre jour."
        )
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        vertexai.init(project=project, location=os.getenv("VERTEX_LOCATION", "us-central1"))
        model = GenerativeModel("gemini-2.0-flash-001")
        resp = model.generate_content(
            "Écris un très court poème en français (4 vers), thème : nuages et code."
        )
        return (resp.text or "").strip()
    except Exception:
        return (
            "Le vent souffle sur les branches.\n"
            "La nuit tombe doucement.\n"
            "Les étoiles veillent là-haut.\n"
            "Demain sera un autre jour."
        )