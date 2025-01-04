"""Custom exceptions for summarization service."""

class SummarizationError(Exception):
    """Base exception for summarization errors."""
    pass

class EmptyContentError(SummarizationError):
    """Raised when document content is empty."""
    pass

class InvalidDocumentError(SummarizationError):
    """Raised when document format is invalid."""
    pass

class ProcessingError(SummarizationError):
    """Raised when processing fails."""
    def __init__(self, message: str, stage: str):
        super().__init__(message)
        self.stage = stage