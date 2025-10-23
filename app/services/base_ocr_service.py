from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseOCRService(ABC):
    """Abstract base class for OCR service providers."""
    
    @abstractmethod
    async def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document using OCR.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Processed document data with extracted information
            
        Raises:
            Exception: If processing fails
        """
        pass
    
    @abstractmethod
    def extract_bank_statement_data(self, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant bank statement data from OCR result.
        
        Args:
            ocr_result: Raw result from OCR provider
            
        Returns:
            Extracted and formatted data with standardized fields:
            - bank_name: str
            - account_holder_name: str
            - account_number: str
            - confidence: float
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the OCR provider."""
        pass
