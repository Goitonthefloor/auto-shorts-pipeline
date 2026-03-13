from fastapi import FastAPI, HTTPException
from .models import RunRequest
from .pipeline import run_pipeline

app = FastAPI(title="Autonomous Shorts Pipeline")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/run")
def run(req: RunRequest):
    try:
        result = run_pipeline(req.instruction)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
