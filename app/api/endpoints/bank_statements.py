from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from models.responses import BankStatementResponse, BankStatementData, ErrorResponse
from services.veryfi_service import VeryfiService
from utils.file_handler import FileHandler
from api.dependencies import get_veryfi_service
from core.config import get_settings, Settings
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/parse-bank-statement",
    response_model=BankStatementResponse,
    summary="Parse Bank Statement",
    description="Upload a bank statement (PDF, JPG, PNG) to extract structured data using OCR",
    responses={
        200: {
            "description": "Document processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": {
                            "bank_name": "Chase Bank",
                            "account_holder_name": "John Doe",
                            "account_number": "****1234",
                            "confidence": 0.95
                        },
                        "message": "Document processed successfully"
                    }
                }
            }
        },
        400: {
            "description": "Invalid file type",
            "model": ErrorResponse
        },
        413: {
            "description": "File too large (max 10MB)",
            "model": ErrorResponse
        },
        500: {
            "description": "Processing error",
            "model": ErrorResponse
        }
    }
)
async def parse_bank_statement(
    file: UploadFile = File(..., description="Bank statement file (PDF, JPG, PNG, max 10MB)"),
    veryfi_service: VeryfiService = Depends(get_veryfi_service),
    settings: Settings = Depends(get_settings)
) -> BankStatementResponse:
    """
    Parse a bank statement and extract key information.
    
    **Extracted Data:**
    - Bank name
    - Account holder name
    - Account number
    - OCR confidence score
    
    **Supported Formats:** PDF, JPEG, PNG (max 10MB)
    """
    temp_file_path = None
    
    try:
        logger.info(f"Received file upload: {file.filename}")
        
        # Validate file type
        FileHandler.validate_file_type(file, settings.allowed_file_types)
        
        # Save file temporarily and get content
        temp_file_path, file_content = await FileHandler.save_upload_file_temp(file)
        
        # Validate file size
        FileHandler.validate_file_size(file_content, settings.max_file_size)
        
        # Process document with Veryfi
        veryfi_result = await veryfi_service.process_document(temp_file_path)
        
        # Extract relevant data
        extracted_data = veryfi_service.extract_bank_statement_data(veryfi_result)
        
        logger.info(f"Successfully processed: {file.filename}")
        return BankStatementResponse(
            status="success",
            data=BankStatementData(**extracted_data),
            message="Document processed successfully"
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error processing bank statement: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
        
    finally:
        if temp_file_path:
            FileHandler.cleanup_temp_file(temp_file_path)
