import logging
from fastapi import FastAPI, Request, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from app.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION, API_KEY
from app.routes import upload, analyze
from app.utils.exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    ImageNotFoundError,
    InvalidAPIKeyError
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key for protected endpoints."""
    if api_key != API_KEY:
        raise InvalidAPIKeyError()
    return api_key


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.url.path} - Client: {request.client.host}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response



app.include_router(upload.router, tags=["Upload"], dependencies=[Depends(verify_api_key)])
app.include_router(analyze.router, tags=["Analysis"], dependencies=[Depends(verify_api_key)])


@app.get("/", tags=["default"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Skin Analysis API",
        "version": APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "upload": "/upload",
            "analyze": "/analyze"
        }
    }


@app.get("/health", tags=["default"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Global exception handlers
@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_handler(request: Request, exc: InvalidFileTypeError):
    logger.error(f"Invalid file type: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(FileSizeExceededError)
async def file_size_exceeded_handler(request: Request, exc: FileSizeExceededError):
    logger.error(f"File size exceeded: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(ImageNotFoundError)
async def image_not_found_handler(request: Request, exc: ImageNotFoundError):
    logger.error(f"Image not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)