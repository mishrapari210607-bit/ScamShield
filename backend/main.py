"""ScamShield HTTP API and static frontend server."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.detector import analyze_message


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(title="ScamShield", description="Check a message for common scam warning signs.")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class AnalyzeRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, object]:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message must not be blank.")
    return analyze_message(message)


@app.get("/", include_in_schema=False)
def homepage() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
