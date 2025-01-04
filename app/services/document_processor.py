from typing import Optional, Dict, Any, List
from datetime import datetime
import magic
from fastapi import UploadFile
from app.models.document import Document
from app.core.config import settings
import hashlib
import os

class DocumentProcessor:
    def __init__(self, storage_path: str = settings.DOCUMENT_STORAGE_PATH):
        self.storage_path = storage_path

    async def process_document(self, file: UploadFile, case_id: int, user_id: int) -> Document:
        """Process an uploaded document and create Document record."""
        # Read file content
        content = await file.read()
        
        # Get file metadata
        file_type = magic.from_buffer(content, mime=True)
        file_size = len(content)
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Generate storage path
        storage_path = self._generate_storage_path(case_id, file_hash, file.filename)
        
        # Save file
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        with open(storage_path, 'wb') as f:
            f.write(content)
        
        # Create document record
        document = Document(
            case_id=case_id,
            filename=file.filename,
            file_type=file_type,
            file_size=file_size,
            storage_path=storage_path,
            submitted_by=user_id,
            metadata={
                'hash': file_hash,
                'original_name': file.filename,
                'upload_timestamp': datetime.utcnow().isoformat()
            }
        )
        
        return document

    def _generate_storage_path(self, case_id: int, file_hash: str, filename: str) -> str:
        """Generate unique storage path for document."""
        ext = os.path.splitext(filename)[1]
        return os.path.join(
            self.storage_path,
            str(case_id),
            f"{file_hash[:8]}{ext}"
        )

    async def extract_metadata(self, document: Document) -> Dict[str, Any]:
        """Extract metadata from document file."""
        metadata = {}
        
        try:
            # Read file content
            with open(document.storage_path, 'rb') as f:
                content = f.read()
            
            # Basic file metadata
            metadata.update({
                'file_size': len(content),
                'mime_type': magic.from_buffer(content, mime=True),
                'hash': hashlib.sha256(content).hexdigest(),
                'last_modified': datetime.fromtimestamp(
                    os.path.getmtime(document.storage_path)
                ).isoformat()
            })
            
            # TODO: Add advanced metadata extraction based on file type
            # This could include EXIF data for images, PDF metadata, etc.
            
            return metadata
        except Exception as e:
            raise ValueError(f"Failed to extract metadata: {str(e)}")