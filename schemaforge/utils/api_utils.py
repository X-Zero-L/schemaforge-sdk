"""
API utility functions for handling HTTP requests, responses, and authentication.
Includes functions for API request building, response parsing, retry logic, etc.
"""

import json
import time
import random
import logging
import platform
from typing import Any, Dict, Callable, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..exceptions.api_error import (
    SchemaForgeError,
    AuthenticationError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
)
from ..version import VERSION


logger = logging.getLogger("schemaforge")


def get_user_agent() -> str:
    """
    Get the user agent string containing SDK version, Python version, and OS information.
    
    Returns:
        User agent string
    """
    python_version = platform.python_version()
    os_name = platform.system()
    os_version = platform.release()
    return f"SchemaForge-Python/{VERSION} Python/{python_version} {os_name}/{os_version}"


def create_session(
    timeout: float = 30.0,
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist: List[int] = [429, 500, 502, 503, 504],
) -> requests.Session:
    """
    Create a configured HTTP session with retry logic and timeout settings.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        backoff_factor: Retry delay factor
        status_forcelist: List of HTTP status codes that should trigger a retry
        
    Returns:
        Configured requests.Session object
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST"],
    )
    
    # Apply retry strategy to session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def handle_api_response(response: requests.Response) -> Dict[str, Any]:
    """
    Handle API response, check for errors and parse JSON response.
    
    Args:
        response: HTTP response object
        
    Returns:
        Parsed JSON response
        
    Raises:
        AuthenticationError: When authentication fails
        APIConnectionError: When there's an API connection error
        RateLimitError: When rate limit is exceeded
        SchemaForgeError: For other API errors
    """
    status_code = response.status_code
    
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        response_json = {}
    
    request_id = response.headers.get("X-Request-ID", "")
    
    # Handle different error cases
    if status_code == 401:
        raise AuthenticationError(
            message="Authentication failed, please check your API key",
            status_code=status_code,
            response=response_json,
            request_id=request_id,
        )
    elif status_code == 404:
        error_message = response_json.get("detail", "API endpoint not found")
        raise SchemaForgeError(
            message=error_message,
            status_code=status_code,
            response=response_json,
            request_id=request_id,
        )
    elif status_code == 422:
        error_message = "Request validation error"
        if "detail" in response_json:
            error_detail = response_json["detail"]
            if isinstance(error_detail, list) and len(error_detail) > 0:
                error_message = str(error_detail)
            elif isinstance(error_detail, str):
                error_message = error_detail
        
        raise SchemaForgeError(
            message=error_message,
            status_code=status_code,
            response=response_json,
            request_id=request_id,
        )
    elif status_code == 429:
        # Extract retry information if available
        retry_after = response.headers.get("Retry-After")
        message = "Request exceeded API rate limit"
        if retry_after:
            message += f", please try again in {retry_after} seconds"
            
        raise RateLimitError(
            message=message,
            status_code=status_code,
            response=response_json,
            request_id=request_id,
            retry_after=retry_after,
        )
    elif status_code >= 500:
        raise APIConnectionError(
            message="Server error, please try again later",
            status_code=status_code,
            response=response_json,
            request_id=request_id,
        )
    elif status_code != 200:
        # Extract error message from response
        error_message = "Unknown error"
        if "detail" in response_json:
            error_message = response_json["detail"]
        elif "error" in response_json:
            if isinstance(response_json["error"], str):
                error_message = response_json["error"]
            elif isinstance(response_json["error"], dict) and "message" in response_json["error"]:
                error_message = response_json["error"]["message"]
        
        raise SchemaForgeError(
            message=error_message,
            status_code=status_code,
            response=response_json,
            request_id=request_id,
        )
    
    return response_json


def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 16.0,
    jitter: bool = True,
) -> Any:
    """
    Retry a function with exponential backoff strategy.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter
        
    Returns:
        Function return value
        
    Raises:
        The last exception if all retries fail
    """
    retries = 0
    while True:
        try:
            return func()
        except (APIConnectionError, APITimeoutError, RateLimitError) as e:
            retries += 1
            if retries > max_retries:
                raise e
            
            # Calculate delay time
            delay = min(initial_delay * (2 ** (retries - 1)), max_delay)
            
            # Use Retry-After value if available in response
            if hasattr(e, "retry_after") and e.retry_after:
                try:
                    delay = float(e.retry_after)
                except (ValueError, TypeError):
                    pass
            
            # Add random jitter (±25%)
            if jitter:
                delay = delay * (0.75 + random.random() * 0.5)
            
            logger.warning(f"Request failed, retrying in {delay:.2f} seconds (attempt {retries}): {str(e)}")
            time.sleep(delay)
        except Exception as e:
            # Don't retry other types of exceptions
            raise e 