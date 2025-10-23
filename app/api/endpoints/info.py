from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Dict, List
from core.config import get_settings, Settings
from services.ocr_service_factory import OCRServiceFactory
from models.enums import OcrProvider

router = APIRouter()


class FileFormat(BaseModel):
    """Supported file format information."""
    mime_type: str
    extensions: List[str]
    description: str


class ApiInfoResponse(BaseModel):
    """API information response."""
    name: str
    version: str
    description: str
    supported_formats: List[FileFormat]
    max_file_size: str
    ocr_providers: Dict[str, List[str]]
    endpoints: Dict[str, str]


@router.get(
    "/info",
    response_model=ApiInfoResponse,
    summary="API Information",
    description="Get API capabilities, supported formats, and available endpoints"
)
async def get_api_info(
    settings: Settings = Depends(get_settings)
) -> ApiInfoResponse:
    """
    Retrieve comprehensive API information.
    
    Includes supported file formats, constraints, and endpoint directory.
    """
    format_mapping = {
        "application/pdf": {
            "extensions": [".pdf"],
            "description": "PDF documents"
        },
        "image/jpeg": {
            "extensions": [".jpg", ".jpeg"],
            "description": "JPEG images"
        },
        "image/png": {
            "extensions": [".png"],
            "description": "PNG images"
        }
    }
    
    supported_formats = [
        FileFormat(
            mime_type=mime_type,
            extensions=info["extensions"],
            description=info["description"]
        )
        for mime_type, info in format_mapping.items()
        if mime_type in settings.allowed_file_types
    ]
    
    return ApiInfoResponse(
        name=settings.app_name,
        version=settings.app_version,
        description="OCR-based bank statement data extraction",
        supported_formats=supported_formats,
        max_file_size=f"{settings.max_file_size / (1024 * 1024):.2f} MB",
        ocr_providers={
            "available": OCRServiceFactory.list_available_providers(),
            "implemented": OCRServiceFactory.get_implemented_providers(),
            "default": OcrProvider.get_default().value
        },
        endpoints={
            "health": "/api/v1/health",
            "info": "/api/v1/info",
            "ocr_providers": "/api/v1/ocr-providers",
            "parse_bank_statement": "/api/v1/parse-bank-statement"
        }
    )
