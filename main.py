"""
ZT Web Studio build API starter.
IMPORTANT: This queues a job only. It does NOT build APKs until connected to a disposable
container/VM runner with Android SDK + JDK + Gradle installed.
Never run untrusted user code on the API web process itself.
"""
import os, re, uuid, time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="ZT Web Studio Cloud Build API", version="0.1.0")
ALLOWED_ORIGINS = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=["GET","POST"], allow_headers=["Content-Type","Authorization"])

class BuildRequest(BaseModel):
    appName: str = Field(min_length=1, max_length=50)
    packageName: str = Field(min_length=3, max_length=180)
    projectType: str = "android-template"
    template: str = "basic-activity"

JOBS = {}  # Replace with Redis/Postgres in production; memory store is demo-only.

@app.get("/")
def health():
    return {"name":"ZT Web Studio Cloud Build API","status":"ok","note":"Build runner not configured"}

@app.post("/api/build", status_code=202)
def create_build(body: BuildRequest):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+", body.packageName):
        raise HTTPException(400, "Invalid Android application ID")
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"jobId":job_id,"status":"queued","appName":body.appName,"packageName":body.packageName,"createdAt":int(time.time())}
    # TODO: enqueue job to isolated worker (Docker/Kubernetes/Cloud Run job).
    return {"jobId":job_id,"status":"queued","message":"API accepted request; isolated Android build runner must be configured before APK output is available."}

@app.get("/api/build/{job_id}")
def get_build(job_id: str):
    if job_id not in JOBS: raise HTTPException(404, "Unknown job ID")
    return JOBS[job_id]
