from enum import Enum


class OcrProvider(str, Enum):
    """Supported OCR service providers."""
    VERYFI = "veryfi"
    
    @classmethod
    def get_default(cls) -> "OcrProvider":
        """Get the default OCR provider."""
        return cls.VERYFI
    
    @classmethod
    def list_available(cls) -> list[str]:
        """List all available provider names."""
        return [provider.value for provider in cls]
