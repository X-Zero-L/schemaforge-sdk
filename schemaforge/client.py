"""
SchemaForge Python SDK Client
Main interface for interacting with the SchemaForge API
"""

import json
import logging
import asyncio
import os
from typing import Any, Dict, List, Optional, Type, TypeVar
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel

from .utils.api_utils import (
    create_session, 
    handle_api_response,
    retry_with_exponential_backoff
)
from .utils.model_loader import load_model_from_code
from .exceptions.api_error import SchemaForgeError
from .models.request import (
    StructuredRequest,
    ModelGenerationRequest,
    ModelFieldDefinition
)
from .models.response import (
    StructureResponse,
    ModelGenerationResponse
)

logger = logging.getLogger("schemaforge")
T = TypeVar('T', bound=BaseModel)


class SchemaForge:
    """
    SchemaForge API Client
    
    Provides methods for structuring data and generating Pydantic models
    using the SchemaForge API.
    
    Attributes:
        api_key: SchemaForge API key
        api_base: Base URL for API requests
        default_model: Default AI model to use
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        default_model: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_jitter: bool = True,
        verbose: bool = False
    ):
        """
        Initialize SchemaForge client
        
        Args:
            api_key: API key for authentication (defaults to SCHEMAFORGE_API_KEY environment variable)
            api_base: Base URL for API requests (defaults to SCHEMAFORGE_API_BASE environment variable)
            default_model: Default AI model to use
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay for retries in seconds
            retry_jitter: Whether to add random jitter to retry delays
            verbose: Whether to enable verbose logging
        """
        # Fill from environment if not provided
        self.api_key = api_key or os.getenv("SCHEMAFORGE_API_KEY") or os.getenv("API_KEY", "")
        self.api_base = api_base or os.getenv("SCHEMAFORGE_API_BASE") or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.default_model = default_model or os.getenv("SCHEMAFORGE_DEFAULT_MODEL", "gpt-4")
        
        # Timeout and retry settings
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_jitter = retry_jitter
        
        # Check if API key is set
        if not self.api_key:
            logger.warning("API key not set. Please provide api_key parameter or set SCHEMAFORGE_API_KEY environment variable.")
        
        # Create HTTP session
        self._session = create_session(
            timeout=self.timeout,
            max_retries=self.max_retries,
            backoff_factor=self.retry_delay,
        )
        
        # Set headers
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        # Thread pool for async requests
        self._thread_pool = ThreadPoolExecutor()
        
        # Configure log level
        if verbose:
            logging.getLogger("schemaforge").setLevel(logging.DEBUG)
    
    def __del__(self):
        """Clean up resources"""
        try:
            if hasattr(self, "_session"):
                self._session.close()
            if hasattr(self, "_thread_pool"):
                self._thread_pool.shutdown(wait=False)
        except Exception:
            pass
    
    #######################
    # Data Structuring Methods
    #######################
    
    def structure(
        self,
        content: str,
        model_class: Type[T],
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None,
        is_need_schema_description: bool = False
    ) -> T:
        """
        Structure text content using a predefined Pydantic model
        
        Args:
            content: The text content to structure
            model_class: Pydantic model class to use for structuring
            system_prompt: Optional system prompt to guide the AI
            model_name: AI model name to use (defaults to self.default_model)
            is_need_schema_description: Whether to include schema description in system prompt
            
        Returns:
            An instance of the specified model_class populated with structured data
            
        Raises:
            SchemaForgeError: When API request fails
        """
        # Get the JSON schema from the Pydantic model
        schema_json = model_class.model_json_schema()
        
        # Create structured request
        request = StructuredRequest(
            content=content,
            schema_description=json.dumps(schema_json),
            system_prompt=system_prompt,
            model_name=model_name or self.default_model,
            is_need_schema_description=is_need_schema_description
        )
        
        # Send request
        endpoint = "/api/v1/structure"
        url = f"{self.api_base}{endpoint}"
        
        def _make_request():
            response = self._session.post(
                url,
                json=request.model_dump(exclude_none=True),
                headers=self._headers,
                timeout=self.timeout
            )
            return handle_api_response(response)
        
        # Send request with retry logic
        result = retry_with_exponential_backoff(
            _make_request,
            max_retries=self.max_retries,
            initial_delay=self.retry_delay,
            jitter=self.retry_jitter,
        )
        
        # Parse response
        response = StructureResponse(**result)
        
        # Check for success
        if not response.success:
            raise SchemaForgeError(f"Failed to structure data: {response.error}")
        
        # Convert the structured data into the model instance
        return model_class.model_validate(response.data)
    
    def generate_model(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[ModelFieldDefinition]] = None,
        llm_model_name: Optional[str] = None
    ) -> ModelGenerationResponse:
        """
        Generate a Pydantic model from sample data
        
        Args:
            sample_data: Sample data to analyze (text, JSON, CSV, etc.)
            model_name: Name for the generated model
            description: Description of what the model represents
            requirements: Optional specific requirements or validation rules
            expected_fields: Optional list of expected fields
            llm_model_name: AI model name to use (defaults to self.default_model)
            
        Returns:
            ModelGenerationResponse containing the generated model code and schema
            
        Raises:
            SchemaForgeError: When API request fails
        """
        # Create model generation request
        request = ModelGenerationRequest(
            sample_data=sample_data,
            model_name=model_name,
            description=description,
            requirements=requirements,
            expected_fields=expected_fields,
            llm_model_name=llm_model_name or self.default_model
        )
        
        # Send request
        endpoint = "/api/v1/generate-model"
        url = f"{self.api_base}{endpoint}"
        
        def _make_request():
            response = self._session.post(
                url,
                json=request.model_dump(exclude_none=True),
                headers=self._headers,
                timeout=self.timeout
            )
            return handle_api_response(response)
        
        # Send request with retry logic
        result = retry_with_exponential_backoff(
            _make_request,
            max_retries=self.max_retries,
            initial_delay=self.retry_delay,
            jitter=self.retry_jitter,
        )
        
        # Parse response
        response = ModelGenerationResponse(**result)
        
        # Check for success
        if not response.success:
            raise SchemaForgeError(f"Failed to generate model: {response.error}")
        
        return response
    
    def load_generated_model(self, response: ModelGenerationResponse) -> Dict[str, Type[BaseModel]]:
        """
        Load all generated models from the response
        
        Args:
            response: ModelGenerationResponse from generate_model()
            
        Returns:
            Dictionary mapping model names to their corresponding Pydantic model classes
            
        Raises:
            SchemaForgeError: When model loading fails
        """
        try:
            # Extract complete model code from response
            code = response.model_code
            if not code:
                raise SchemaForgeError("No model code found in response")
            
            # Load all models
            models = load_model_from_code(code)
            if not isinstance(models, dict):
                # If only one model is returned, wrap it in a dictionary
                models = {response.model_name: models}
            
            return models
        except Exception as e:
            raise SchemaForgeError(f"Failed to load generated models: {str(e)}")
    
    def get_model_code(self, response: ModelGenerationResponse) -> str:
        """
        Get the complete model code including all dependencies and sub-models
        
        Args:
            response: ModelGenerationResponse from generate_model()
            
        Returns:
            Complete Python code string including all model definitions, dependencies, and sub-models
            
        Raises:
            SchemaForgeError: When code extraction fails
        """
        try:
            # Extract complete model code from response
            code = response.model_code
            if not code:
                raise SchemaForgeError("No model code found in response")
            return code
        except Exception as e:
            raise SchemaForgeError(f"Failed to get model code: {str(e)}")
    
    def get_main_model(self, response: ModelGenerationResponse) -> Type[BaseModel]:
        """
        Get only the main requested model from the response
        
        Args:
            response: ModelGenerationResponse from generate_model()
            
        Returns:
            The main requested Pydantic model class
            
        Raises:
            SchemaForgeError: When model loading fails
        """
        try:
            models = self.load_generated_model(response)
            if response.model_name not in models:
                raise SchemaForgeError(f"Main model '{response.model_name}' not found in generated models")
            return models[response.model_name]
        except Exception as e:
            raise SchemaForgeError(f"Failed to get main model: {str(e)}")
    
    #######################
    # Asynchronous Methods
    #######################
    
    async def astructure(
        self,
        content: str,
        model_class: Type[T],
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> T:
        """
        Asynchronous version of structure method
        
        Args:
            content: The text content to structure
            model_class: Pydantic model class to use for structuring
            system_prompt: Optional system prompt to guide the AI
            model_name: AI model name to use (defaults to self.default_model)
            
        Returns:
            An instance of the specified model_class populated with structured data
            
        Raises:
            SchemaForgeError: When API request fails
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._thread_pool,
            lambda: self.structure(
                content=content,
                model_class=model_class,
                system_prompt=system_prompt,
                model_name=model_name
            )
        )
    
    async def agenerate_model(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[ModelFieldDefinition]] = None,
        llm_model_name: Optional[str] = None
    ) -> ModelGenerationResponse:
        """
        Asynchronous version of generate_model method
        
        Args:
            sample_data: Sample data to analyze (text, JSON, CSV, etc.)
            model_name: Name for the generated model
            description: Description of what the model represents
            requirements: Optional specific requirements or validation rules
            expected_fields: Optional list of expected fields
            llm_model_name: AI model name to use (defaults to self.default_model)
            
        Returns:
            ModelGenerationResponse containing the generated model code and schema
            
        Raises:
            SchemaForgeError: When API request fails
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._thread_pool,
            lambda: self.generate_model(
                sample_data=sample_data,
                model_name=model_name,
                description=description,
                requirements=requirements,
                expected_fields=expected_fields,
                llm_model_name=llm_model_name
            )
        ) 