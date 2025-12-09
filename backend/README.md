# ControlDoc Backend

Base scaffold for the ControlDoc API using FastAPI, PostgreSQL, and MinIO. Logic will be layered into routers/services incrementally.

## Run locally

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables can be provided via a `.env` file. See `app/core/config.py` for available settings.
