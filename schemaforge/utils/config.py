"""
Configuration utilities for the SchemaForge SDK.

This module provides classes for configuring the SchemaForge client
with various options such as API keys, base URLs, timeouts, etc.
"""

import os
from typing import Dict, Any, TypedDict
from dataclasses import dataclass


class ConfigDict(TypedDict, total=False):
    """Type definition for configuration options."""
    
    api_key: str
    api_base: str
    default_model: str
    timeout: int
    max_retries: int
    retry_delay: float
    retry_jitter: float
    user_agent: str
    verbose: bool


@dataclass
class Config:
    """
    Configuration for the SchemaForge client.
    
    Attributes:
        api_key: API key for authentication with SchemaForge
        api_base: Base URL for the SchemaForge API
        default_model: Default AI model to use for requests
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts for transient errors
        retry_delay: Base delay between retries in seconds
        retry_jitter: Random jitter to add to retry delays
        user_agent: Custom user agent string for API requests
        verbose: Whether to enable verbose logging
    """
    
    # Default values
    DEFAULT_API_BASE = "http://localhost:8000"
    DEFAULT_MODEL = "openai:gpt-4o"
    DEFAULT_TIMEOUT = 600  # seconds
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1.0  # seconds
    DEFAULT_RETRY_JITTER = 0.1  # seconds
    DEFAULT_USER_AGENT = f"schemaforge-python-sdk/{os.getenv('SCHEMAFORGE_VERSION', '0.1.0')}"
    
    api_key: str
    api_base: str = DEFAULT_API_BASE
    default_model: str = DEFAULT_MODEL
    timeout: int = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    retry_delay: float = DEFAULT_RETRY_DELAY
    retry_jitter: float = DEFAULT_RETRY_JITTER
    user_agent: str = DEFAULT_USER_AGENT
    verbose: bool = False
    
    @classmethod
    def from_env(cls) -> 'Config':
        """
        Create a configuration object from environment variables.
        
        Environment variables:
            SCHEMAFORGE_API_KEY: API key for authentication
            SCHEMAFORGE_API_BASE: Base URL for the SchemaForge API
            SCHEMAFORGE_DEFAULT_MODEL: Default AI model to use
            SCHEMAFORGE_TIMEOUT: Request timeout in seconds
            SCHEMAFORGE_MAX_RETRIES: Maximum number of retry attempts
            SCHEMAFORGE_VERBOSE: Set to "true" to enable verbose logging
        
        Returns:
            A Config object populated with values from environment variables
        """
        return cls(
            api_key=os.getenv("SCHEMAFORGE_API_KEY", os.getenv("API_KEY", "")),
            api_base=os.getenv("SCHEMAFORGE_API_BASE", os.getenv("API_BASE_URL", cls.DEFAULT_API_BASE)),
            default_model=os.getenv("SCHEMAFORGE_DEFAULT_MODEL", cls.DEFAULT_MODEL),
            timeout=int(os.getenv("SCHEMAFORGE_TIMEOUT", str(cls.DEFAULT_TIMEOUT))),
            max_retries=int(os.getenv("SCHEMAFORGE_MAX_RETRIES", str(cls.DEFAULT_MAX_RETRIES))),
            verbose=os.getenv("SCHEMAFORGE_VERBOSE", "").lower() in ("true", "1", "yes")
        )
    
    @classmethod
    def from_dict(cls, config_dict: ConfigDict) -> 'Config':
        """
        Create a configuration object from a dictionary.
        
        Args:
            config_dict: Dictionary containing configuration options
        
        Returns:
            A Config object populated with values from the dictionary
        """
        config = cls(api_key=config_dict.get("api_key", ""))
        
        # Update fields from dictionary if provided
        for field_name, field_value in config_dict.items():
            if field_name != "api_key" and hasattr(config, field_name):
                setattr(config, field_name, field_value)
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dictionary containing configuration options
        """
        return {
            "api_key": self.api_key,
            "api_base": self.api_base,
            "default_model": self.default_model,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "retry_jitter": self.retry_jitter,
            "user_agent": self.user_agent,
            "verbose": self.verbose
        }
        
    def __str__(self) -> str:
        """String representation of the configuration with the API key masked."""
        masked_dict = self.to_dict()
        if self.api_key:
            masked_dict["api_key"] = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "****"
        return str(masked_dict) 