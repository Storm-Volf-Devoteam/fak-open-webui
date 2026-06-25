import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

FLUX_URL = os.getenv(
    "FLUX_URL", "https://inference.datacrunch.io/flux2-klein-9b/generate"
)


def parse_size(size: str) -> tuple[int, int]:
    try:
        w, h = size.lower().split("x")
        w, h = int(w), int(h)
        w = max(16, (w // 16) * 16)
        h = max(16, (h // 16) * 16)
        return w, h
    except Exception:
        return 1024, 768


@app.post("/v1/images/generations")
async def generate(request: Request):
    auth = request.headers.get("Authorization", "")
    body = await request.json()

    prompt = body.get("prompt", "")
    size = body.get("size", "1024x768")
    n = body.get("n", 1)

    width, height = parse_size(size)

    flux_payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "enable_base64_output": True,
    }

    images = []
    async with httpx.AsyncClient(timeout=120) as client:
        for _ in range(n):
            resp = await client.post(
                FLUX_URL,
                json=flux_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": auth,
                },
            )
            if resp.status_code != 200:
                return JSONResponse(
                    status_code=resp.status_code,
                    content={"error": resp.text},
                )
            data = resp.json()
            images.append({"b64_json": data["image"]})

    return {"created": 0, "data": images}


@app.get("/v1/models")
async def models():
    return {
        "data": [
            {
                "id": "flux2-klein-9b",
                "object": "model",
                "owned_by": "datacrunch",
            }
        ]
    }
