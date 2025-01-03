"""Custom exceptions for the AI ETL pipeline."""

class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class DocumentProcessingError(PipelineError):
    """Raised when document processing fails."""
    pass

class DocumentValidationError(PipelineError):
    """Raised when document validation fails."""
    pass

class BatchProcessingError(PipelineError):
    """Raised when batch processing fails."""
    def __init__(self, message: str, errors: list):
        super().__init__(message)
        self.errors = errors