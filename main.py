from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from routes.JDendpoints import router as JD_router
from utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Application startup")
    yield
    # Shutdown actions
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan, title="ByticalGPT API", description="API for managing HR tasks", version="0.1")

# Include the router for template endpoints
app.include_router(JD_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1, reload=True)