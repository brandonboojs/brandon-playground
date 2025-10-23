from pydantic import BaseModel, Field
from typing import Optional


class BankStatementData(BaseModel):
    """Extracted bank statement data."""
    
    bank_name: Optional[str] = Field(None, description="Name of the bank")
    account_holder_name: Optional[str] = Field(None, description="Account holder's name")
    account_number: Optional[str] = Field(None, description="Bank account number")
    confidence: float = Field(0.0, description="OCR confidence score", ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "bank_name": "Chase Bank",
                "account_holder_name": "John Doe",
                "account_number": "****1234",
                "confidence": 0.95
            }
        }


class BankStatementResponse(BaseModel):
    """API response for bank statement parsing."""
    
    status: str = Field(..., description="Processing status")
    data: BankStatementData = Field(..., description="Extracted bank statement data")
    message: Optional[str] = Field(None, description="Additional information")
    provider: Optional[str] = Field(None, description="OCR provider used for processing")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "bank_name": "Chase Bank",
                    "account_holder_name": "John Doe",
                    "account_number": "****1234",
                    "confidence": 0.95
                },
                "message": "Document processed successfully",
                "provider": "veryfi"
            }
        }


class ErrorResponse(BaseModel):
    """API error response."""
    
    status: str = Field("error", description="Error status")
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "detail": "Invalid file type",
                "error_code": "INVALID_FILE_TYPE"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "doc-processor",
                "version": "2.0.0"
            }
        }
