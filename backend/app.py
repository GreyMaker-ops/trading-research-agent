from fastapi import FastAPI

app = FastAPI(title="Trading Research Agent")


@app.get("/health")
async def health():
    return {"status": "ok"}
