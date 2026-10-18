import time
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send

EMAIL = "23f2001912@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-1dlfvd.example.com"

api = FastAPI(title="Statistics API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@api.get("/stats")
def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        parts = values.split(",")
        if not parts or any(part.strip() == "" for part in parts):
            raise ValueError("empty integer")
        numbers = [int(part.strip()) for part in parts]
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    total = sum(numbers)
    count = len(numbers)
    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }

@api.get("/health")
def health():
    return {"ok": True}

class RequestHeadersMiddleware:
    """Outer middleware adds headers to normal, error, and CORS preflight responses."""
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        started = time.perf_counter()

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - started)
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode("ascii")))
                headers.append((b"x-process-time", f"{elapsed:.6f}".encode("ascii")))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)

# Wrap the entire FastAPI/CORS stack so every response gets both middleware headers.
app = RequestHeadersMiddleware(api)
