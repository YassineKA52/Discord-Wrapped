from fastapi import FastAPI
from api.routes import stats, recap

app = FastAPI(title="Discord Wrapped API")

app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.include_router(recap.router, prefix="/recap", tags=["Recap"])

@app.get("/")
async def root():
    return {"status": "online", "message": "Discord Wrapped API is running"}