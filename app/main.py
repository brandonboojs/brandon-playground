from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from core.config import get_settings
from core.logging import setup_logging, get_logger
from api.endpoints import health, bank_statements, info

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Validate credentials at startup
if not all([
    settings.veryfi_client_id,
    settings.veryfi_client_secret,
    settings.veryfi_username,
    settings.veryfi_api_key
]):
    logger.error("Missing Veryfi credentials in environment variables")
    raise ValueError("Missing Veryfi credentials. Please set them in your .env file.")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="OCR-based API for extracting structured data from bank statements",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


def custom_openapi():
    """Custom OpenAPI schema with clean, organized documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description=app.description,
        routes=app.routes,
        contact=app.contact,
        license_info=app.license_info,
    )
    
    # Enhanced API information
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add security schemes for future implementation
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key for authentication (coming soon)"
        }
    }
    
    # Clean tag descriptions
    openapi_schema["tags"] = [
        {
            "name": "Root",
            "description": "API overview and navigation"
        },
        {
            "name": "Health",
            "description": "Service health monitoring"
        },
        {
            "name": "Information",
            "description": "API capabilities and metadata"
        },
        {
            "name": "Bank Statements",
            "description": "Bank statement OCR processing"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(info.router, prefix="/api/v1", tags=["Information"])
app.include_router(bank_statements.router, prefix="/api/v1", tags=["Bank Statements"])


@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info("Shutting down application")


@app.get(
    "/",
    tags=["Root"],
    summary="API Overview",
    response_description="API metadata and navigation links"
)
async def root():
    """Get API information and available endpoints."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "health": "/api/v1/health",
            "info": "/api/v1/info",
            "parse_bank_statement": "/api/v1/parse-bank-statement"
        }
    }
