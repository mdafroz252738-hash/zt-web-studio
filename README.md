# ZT Web Studio — Full IDE starter (mobile-first)

This bundle extends the original web editor with:
- HTML/CSS/JS editor, live sandboxed preview, starter templates, local browser project saving
- AI endpoint client scaffold (Cloudflare Worker + Gemini API secret)
- Android Cloud Builder UI scaffold
- FastAPI build API scaffold that validates and queues build requests
- Minimal native Android Gradle project template

## Important status
This is a **starter/scaffold**, not a deployed production IDE. AI can work after deploying the Worker and configuring a Gemini API key. The build API currently queues a job but does NOT compile an APK. A secure isolated build runner is still required. Do not tell users APK builds work until the runner has been implemented and tested.

## Quick start on a phone
1. Download and extract `ZT_Web_Studio_Full_Starter.zip`.
2. Upload `index.html` to a GitHub repository and enable Settings → Pages → Deploy from a branch → `main` → `/(root)`.
3. Open the published site and test HTML/CSS/JS editor, templates, preview, reset and download.
4. The site is static; local project saves stay in the same browser/device.

## Enable AI code generation
1. Create a Cloudflare Worker using `backend/ai-worker.js`.
2. Add Worker secret `GEMINI_API_KEY` in Settings → Variables and Secrets.
3. Deploy it and set the website AI endpoint to `https://YOUR-WORKER.workers.dev/generate`.
4. For production, restrict `Access-Control-Allow-Origin` to your exact Pages domain and add per-user rate limits/authentication.

## Cloud build architecture (recommended)
Browser → authenticated API → queue → isolated one-job Android build container → artifact storage → short-lived download URL.

Never execute user-provided build scripts in the API web process. Each job should run in a disposable container/VM with CPU/memory/time limits, no privileged mode, restricted outbound network, non-root user, dependency cache policy, and workspace cleanup. Store artifacts privately and provide short-lived signed URLs. Add auth, quotas, abuse controls, logs and deletion policy.

### API scaffold
`backend/main.py` is a FastAPI starter:
- `GET /` health check
- `POST /api/build` creates a queued job ID
- `GET /api/build/{job_id}` returns its current state

Run locally with Python 3.11+:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
Set `ALLOWED_ORIGINS` to the real website origin. The current in-memory queue is only a demo and resets on restart. It does not compile APKs.

## Native Android starter
`android-template/` contains a minimal Kotlin Android app project with Gradle files. Open it in Android Studio or use it as the first template for the isolated build runner. Ensure installed JDK/Gradle/Android SDK versions match the Android Gradle Plugin requirements.

## Production milestones
1. Auth and user accounts (Clerk/Supabase/Auth0 or equivalent).
2. Persistent projects in a database/object storage (Postgres + S3/R2).
3. Monaco editor or CodeMirror for robust editing and language support.
4. AI project/file edits with schema validation, quotas, and audit logs.
5. Build queue + isolated runner + artifact storage + status polling.
6. Signing key management (never expose keystore/password to browser), APK signing, security scanning, retention/deletion and rate limits.
7. Tests, monitoring, backups, privacy policy and terms.

## Security notes
- Never put Gemini API keys, signing keystores, or server credentials in frontend JavaScript.
- Treat AI-generated code and uploaded projects as untrusted.
- This preview sandbox is not a substitute for a server-side sandbox.
