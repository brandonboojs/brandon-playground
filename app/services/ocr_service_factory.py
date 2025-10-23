from typing import Dict, Optional
from models.enums import OcrProvider
from services.base_ocr_service import BaseOCRService
from services.veryfi_service import VeryfiService
from core.config import Settings
from core.logging import get_logger

logger = get_logger(__name__)


class OCRServiceFactory:
    """Factory for creating OCR service instances based on provider type."""
    
    _instances: Dict[OcrProvider, BaseOCRService] = {}
    
    @classmethod
    def get_service(
        cls, 
        provider: OcrProvider, 
        settings: Optional[Settings] = None
    ) -> BaseOCRService:
        """
        Get or create an OCR service instance.
        
        Uses singleton pattern to cache service instances.
        
        Args:
            provider: OCR provider enum value
            settings: Application settings (required for Veryfi)
            
        Returns:
            OCR service instance
            
        Raises:
            ValueError: If provider is not supported or settings missing
        """
        # Return cached instance if available
        if provider in cls._instances:
            logger.debug(f"Returning cached {provider.value} service")
            return cls._instances[provider]
        
        # Create new instance based on provider
        logger.info(f"Creating new {provider.value} service instance")
        
        if provider == OcrProvider.VERYFI:
            if not settings:
                raise ValueError("Settings required for Veryfi service")
            service = VeryfiService(settings)
        
        else:
            raise ValueError(f"Unsupported OCR provider: {provider}")
        
        # Cache and return the instance
        cls._instances[provider] = service
        return service
    
    @classmethod
    def list_available_providers(cls) -> list[str]:
        """List all available OCR providers."""
        return OcrProvider.list_available()
    
    @classmethod
    def get_implemented_providers(cls) -> list[str]:
        """List currently implemented OCR providers."""
        return [
            OcrProvider.VERYFI.value
        ]
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached service instances."""
        logger.info("Clearing OCR service cache")
        cls._instances.clear()
