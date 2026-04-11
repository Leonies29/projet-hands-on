@app.get("/hello")
def hello():
    return {"message": "Bienvenue sur notre API !"}
 
 
@app.get("/status")
def status():
    return {
        "status": "ok",
        "datetime": datetime.now().isoformat()
    }
 
 
@app.get("/data")
def get_data():
    try:
        data = read_data()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.post("/data", status_code=201)
def post_data(entry: DataEntry):
    try:
        write_data(entry.dict())
        return {"message": "Entrée ajoutée avec succès", "entry": entry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/poem")
def poem():
    try:
        generated = generate_poem()
        return {"poem": generated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))