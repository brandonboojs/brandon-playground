from veryfi import Client
from typing import Dict, Any
from core.config import Settings
from core.logging import get_logger
from services.base_ocr_service import BaseOCRService

logger = get_logger(__name__)


class VeryfiService(BaseOCRService):
    """Service for interacting with Veryfi OCR API."""
    
    def __init__(self, settings: Settings):
        """
        Initialize Veryfi client.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.client = Client(
            client_id=settings.veryfi_client_id,
            client_secret=settings.veryfi_client_secret,
            username=settings.veryfi_username,
            api_key=settings.veryfi_api_key
        )
        logger.info("Veryfi OCR service initialized")
    
    async def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document using Veryfi OCR.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Processed document data
            
        Raises:
            Exception: If processing fails
        """
        try:
            logger.info(f"Processing document with Veryfi: {file_path}")
            
            # Process document with Veryfi
            result = self.client.process_document(
                file_path,
                categories=["bank_statement"]
            )
            
            logger.info(f"Veryfi processing complete. Confidence: {result.get('confidence', 0.0)}")
            return result
            
        except Exception as e:
            logger.error(f"Veryfi processing error: {str(e)}", exc_info=True)
            raise
    
    def extract_bank_statement_data(self, veryfi_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant bank statement data from Veryfi result.
        
        Args:
            veryfi_result: Raw result from Veryfi API
            
        Returns:
            Extracted and formatted data
        """
        logger.debug(f"Extracting data from Veryfi result")
        
        extracted_data = {
            "bank_name": veryfi_result.get("vendor"),
            "account_holder_name": veryfi_result.get("account_holder_name"),
            "account_number": veryfi_result.get("account_number"),
            "confidence": veryfi_result.get("confidence", 0.0),
        }
        
        logger.debug(f"Extracted data: {extracted_data}")
        return extracted_data
    
    def get_provider_name(self) -> str:
        """Get the name of the OCR provider."""
        return "Veryfi"
