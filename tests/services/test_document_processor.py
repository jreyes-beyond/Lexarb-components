import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from fastapi import UploadFile
from app.services.document_processor import DocumentProcessor
from app.models.document import Document

@pytest.fixture
def document_processor():
    return DocumentProcessor(storage_path="/test/storage")

@pytest.fixture
def mock_upload_file():
    file = Mock(spec=UploadFile)
    file.filename = "test_document.pdf"
    return file

@pytest.mark.asyncio
async def test_process_document(document_processor, mock_upload_file):
    # Setup
    case_id = 1
    user_id = 2
    file_content = b"test content"
    mock_upload_file.read.return_value = file_content
    
    with patch('magic.from_buffer', return_value='application/pdf'), \
         patch('os.makedirs'), \
         patch('builtins.open', mock_open()):
        
        # Execute
        document = await document_processor.process_document(
            mock_upload_file,
            case_id,
            user_id
        )
        
        # Assert
        assert document.case_id == case_id
        assert document.submitted_by == user_id
        assert document.filename == "test_document.pdf"
        assert document.file_type == "application/pdf"
        assert document.file_size == len(file_content)
        assert document.metadata['original_name'] == "test_document.pdf"
        assert 'hash' in document.metadata
        assert 'upload_timestamp' in document.metadata

@pytest.mark.asyncio
async def test_extract_metadata(document_processor):
    # Setup
    document = Document(
        case_id=1,
        filename="test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/test/storage/1/test.pdf"
    )
    
    file_content = b"test content"
    mock_stat = Mock()
    mock_stat.st_mtime = datetime.now().timestamp()
    
    with patch('builtins.open', mock_open(read_data=file_content)), \
         patch('os.path.getmtime', return_value=mock_stat.st_mtime), \
         patch('magic.from_buffer', return_value='application/pdf'):
        
        # Execute
        metadata = await document_processor.extract_metadata(document)
        
        # Assert
        assert metadata['file_size'] == len(file_content)
        assert metadata['mime_type'] == 'application/pdf'
        assert 'hash' in metadata
        assert 'last_modified' in metadata

def test_generate_storage_path(document_processor):
    # Setup
    case_id = 1
    file_hash = "abcdef1234567890"
    filename = "test_document.pdf"
    
    # Execute
    storage_path = document_processor._generate_storage_path(
        case_id,
        file_hash,
        filename
    )
    
    # Assert
    expected_path = f"/test/storage/1/{file_hash[:8]}.pdf"
    assert storage_path == expected_path

@pytest.mark.asyncio
async def test_process_document_with_invalid_file(document_processor, mock_upload_file):
    # Setup
    case_id = 1
    user_id = 2
    mock_upload_file.read.side_effect = Exception("Failed to read file")
    
    # Execute and Assert
    with pytest.raises(Exception):
        await document_processor.process_document(
            mock_upload_file,
            case_id,
            user_id
        )

@pytest.mark.asyncio
async def test_extract_metadata_with_missing_file(document_processor):
    # Setup
    document = Document(
        case_id=1,
        filename="missing.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/test/storage/1/missing.pdf"
    )
    
    # Execute and Assert
    with pytest.raises(ValueError, match="Failed to extract metadata"):
        await document_processor.extract_metadata(document)