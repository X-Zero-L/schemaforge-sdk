"""
SchemaForge Python SDK 
Official Python SDK for SchemaForge AI (https://github.com/X-Zero-L/schemaforge-ai).
A tool for simplifying interactions with the SchemaForge API, providing data structuring and model generation capabilities
"""

# Version information
from .version import VERSION as __version__

# Export client class
from .client import SchemaForge

# Export config class
from .utils.config import Config

# Export exception classes
from .exceptions.api_error import (
    SchemaForgeError,
    ValidationError,
    AuthenticationError,
    APIConnectionError,
    APITimeoutError,
    ModelError,
    RateLimitError
)

# Export utility functions
from .utils.model_loader import load_model_from_code

__all__ = [
    "SchemaForge",
    "Config",
    "SchemaForgeError",
    "ValidationError",
    "AuthenticationError",
    "APIConnectionError",
    "APITimeoutError",
    "ModelError",
    "RateLimitError",
    "load_model_from_code"
] 