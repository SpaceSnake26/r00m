from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router as pages_router
from app.api import router as api_router
from app.config import config
import app.puzzles # Triggers registration

app = FastAPI(
    title="r00m",
    description="Captive Portal Escape Room",
    docs_url=None if not config.DEBUG else "/docs",
    redoc_url=None
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(pages_router)
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=config.DEBUG)
