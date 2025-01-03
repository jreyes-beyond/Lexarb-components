import magic
from typing import List
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class DocumentValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.endswith("/submit") and request.method == "POST":
            # Validate content length
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > settings.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
                )
            
            # Get the form data and validate file type
            form = await request.form()
            if "file" in form:
                file = form["file"]
                content = await file.read()
                mime_type = magic.from_buffer(content, mime=True)
                
                if mime_type not in settings.ALLOWED_MIME_TYPES:
                    raise HTTPException(
                        status_code=415,
                        detail=f"File type {mime_type} not allowed. Allowed types: {settings.ALLOWED_MIME_TYPES}"
                    )
                
                # Reset file position for subsequent reads
                await file.seek(0)
        
        return await call_next(request)