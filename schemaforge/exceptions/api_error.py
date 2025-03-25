"""
Exception classes for the SchemaForge SDK.

This module provides a comprehensive set of custom exceptions for different
error cases that may occur when using the SchemaForge API.
"""

from typing import Dict, Any, Optional


class SchemaForgeError(Exception):
    """Base exception class for all SchemaForge-related errors."""
    
    def __init__(self, message: str, *, status_code: Optional[int] = None, 
                 response: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        self.request_id = request_id or self.response.get("request_id")
        
    def __str__(self) -> str:
        msg = self.message
        if self.status_code is not None:
            msg = f"[{self.status_code}] {msg}"
        if self.request_id is not None:
            msg = f"{msg} (request_id: {self.request_id})"
        return msg


class ValidationError(SchemaForgeError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, *, field_errors: Optional[Dict[str, str]] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.field_errors = field_errors or {}


class AuthenticationError(SchemaForgeError):
    """Raised when authentication with the SchemaForge API fails."""
    
    def __init__(self, message: str = "Authentication failed. Please check your API key.", **kwargs):
        super().__init__(message, **kwargs)


class APIConnectionError(SchemaForgeError):
    """Raised when there's a problem connecting to the SchemaForge API."""
    
    def __init__(self, message: str = "Error connecting to SchemaForge API.", *, 
                 original_error: Optional[Exception] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.original_error = original_error
        
    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.original_error:
            return f"{base_msg} Original error: {str(self.original_error)}"
        return base_msg


class APITimeoutError(APIConnectionError):
    """Raised when a request to the SchemaForge API times out."""
    
    def __init__(self, message: str = "Request to SchemaForge API timed out.", **kwargs):
        super().__init__(message, **kwargs)


class ModelError(SchemaForgeError):
    """Raised when there's an error with the model generation or usage."""
    
    def __init__(self, message: str, *, model_name: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.model_name = model_name
        
    def __str__(self) -> str:
        if self.model_name:
            return f"{super().__str__()} (model: {self.model_name})"
        return super().__str__()


class RateLimitError(SchemaForgeError):
    """Raised when the rate limit for the SchemaForge API is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded.", *, 
                 retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
        
    def __str__(self) -> str:
        msg = super().__str__()
        if self.retry_after:
            return f"{msg} Try again in {self.retry_after} seconds."
        return msg 