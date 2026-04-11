import os


def generate_poem() -> str:
    project = os.getenv("GCP_PROJECT", "").strip()
    location = os.getenv("VERTEX_LOCATION", "europe-west1").strip()
    if not project:
        return (
            "Le vent souffle sur les branches.\n"
            "La nuit tombe doucement.\n"
            "Les étoiles veillent là-haut.\n"
            "Demain sera un autre jour."
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
        raise RuntimeError("Réponse vide")
    return text
