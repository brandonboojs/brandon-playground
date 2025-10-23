import tempfile
import os
from pathlib import Path
from typing import BinaryIO
from fastapi import UploadFile, HTTPException
from core.logging import get_logger

logger = get_logger(__name__)


class FileHandler:
    """Utility class for handling file operations."""
    
    @staticmethod
    def validate_file_type(file: UploadFile, allowed_types: list) -> None:
        """
        Validate uploaded file type.
        
        Args:
            file: Uploaded file
            allowed_types: List of allowed MIME types
            
        Raises:
            HTTPException: If file type is not allowed
        """
        if file.content_type not in allowed_types:
            logger.warning(
                f"Invalid file type uploaded: {file.content_type}. "
                f"Allowed types: {allowed_types}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        logger.debug(f"File type validated: {file.content_type}")
    
    @staticmethod
    def validate_file_size(file_content: bytes, max_size: int) -> None:
        """
        Validate file size.
        
        Args:
            file_content: File content as bytes
            max_size: Maximum allowed file size in bytes
            
        Raises:
            HTTPException: If file exceeds size limit
        """
        file_size = len(file_content)
        if file_size > max_size:
            logger.warning(
                f"File size {file_size} bytes exceeds limit of {max_size} bytes"
            )
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {max_size / (1024 * 1024):.2f}MB"
            )
        logger.debug(f"File size validated: {file_size} bytes")
    
    @staticmethod
    async def save_upload_file_temp(
        upload_file: UploadFile
    ) -> tuple[str, bytes]:
        """
        Save uploaded file to temporary location.
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            Tuple of (temp_file_path, file_content)
        """
        try:
            # Read file content
            file_content = await upload_file.read()
            
            # Get file extension
            file_extension = Path(upload_file.filename).suffix
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            logger.info(f"File saved to temporary location: {temp_path}")
            return temp_path, file_content
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error saving file: {str(e)}"
            )
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """
        Remove temporary file.
        
        Args:
            file_path: Path to temporary file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Temporary file removed: {file_path}")
        except Exception as e:
            logger.error(f"Error removing temporary file: {str(e)}", exc_info=True)
