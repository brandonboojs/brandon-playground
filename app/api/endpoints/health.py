from fastapi import APIRouter, Depends
from models.responses import HealthResponse
from core.config import get_settings, Settings

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the service is running and healthy"
)
async def health_check(
    settings: Settings = Depends(get_settings)
) -> HealthResponse:
    """
    Service health status endpoint.
    
    Use this for monitoring, load balancer health checks, and service discovery.
    """
    return HealthResponse(
        status="healthy",
        service="doc-processor",
        version=settings.app_version
    )
