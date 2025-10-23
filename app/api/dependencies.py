from fastapi import Depends
from core.config import get_settings, Settings
from services.base_ocr_service import BaseOCRService
from services.ocr_service_factory import OCRServiceFactory
from models.enums import OcrProvider


def get_ocr_service(
    provider: OcrProvider,
    settings: Settings = Depends(get_settings)
) -> BaseOCRService:
    """
    Dependency for getting OCR service instance based on provider.
    
    Uses factory pattern with caching for performance.
    
    Args:
        provider: OCR provider enum value
        settings: Application settings
        
    Returns:
        BaseOCRService instance for the specified provider
        
    Raises:
        ValueError: If provider is not supported
        NotImplementedError: If provider is not yet implemented
    """
    return OCRServiceFactory.get_service(provider, settings)
