# API Reference

This document provides detailed information about the SchemaForge SDK API.

## SchemaForge Client

The main interface for interacting with the SchemaForge API.

### Constructor

```python
SchemaForge(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    default_model: Optional[str] = None,
    timeout: float = 60.0,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    retry_jitter: bool = True,
    verbose: bool = False
)
```

**Parameters:**
- `api_key`: API key for authentication (defaults to SCHEMAFORGE_API_KEY environment variable)
- `api_base`: Base URL for API requests (defaults to SCHEMAFORGE_API_BASE environment variable)
- `default_model`: Default AI model to use
- `timeout`: Request timeout in seconds
- `max_retries`: Maximum number of retry attempts
- `retry_delay`: Initial delay for retries in seconds
- `retry_jitter`: Whether to add random jitter to retry delays
- `verbose`: Whether to enable verbose logging

## Data Structuring Methods

### structure

```python
structure(
    content: str,
    model_class: Type[T],
    system_prompt: Optional[str] = None,
    model_name: Optional[str] = None,
    is_need_schema_description: bool = False
) -> T
```

Structure text content using a predefined Pydantic model.

**Parameters:**
- `content`: The text content to structure
- `model_class`: Pydantic model class to use for structuring
- `system_prompt`: Optional system prompt to guide the AI
- `model_name`: AI model name to use (defaults to self.default_model)
- `is_need_schema_description`: Whether to include schema description in system prompt

**Returns:**
- An instance of the specified model_class populated with structured data

**Raises:**
- `SchemaForgeError`: When API request fails

### astructure

```python
astructure(
    content: str,
    model_class: Type[T],
    system_prompt: Optional[str] = None,
    model_name: Optional[str] = None
) -> T
```

Asynchronous version of structure method.

## Model Generation Methods

### generate_model

```python
generate_model(
    sample_data: str,
    model_name: str,
    description: str,
    requirements: Optional[str] = None,
    expected_fields: Optional[List[ModelFieldDefinition]] = None,
    llm_model_name: Optional[str] = None
) -> ModelGenerationResponse
```

Generate a Pydantic model from sample data.

**Parameters:**
- `sample_data`: Sample data to analyze (text, JSON, CSV, etc.)
- `model_name`: Name for the generated model
- `description`: Description of what the model represents
- `requirements`: Optional specific requirements or validation rules
- `expected_fields`: Optional list of expected fields
- `llm_model_name`: AI model name to use (defaults to self.default_model)

**Returns:**
- `ModelGenerationResponse` containing the generated model code and schema

**Raises:**
- `SchemaForgeError`: When API request fails

### agenerate_model

```python
agenerate_model(
    sample_data: str,
    model_name: str,
    description: str,
    requirements: Optional[str] = None,
    expected_fields: Optional[List[ModelFieldDefinition]] = None,
    llm_model_name: Optional[str] = None
) -> ModelGenerationResponse
```

Asynchronous version of generate_model method.

## Model Handling Methods

### load_generated_model

```python
load_generated_model(
    response: ModelGenerationResponse
) -> Dict[str, Type[BaseModel]]
```

Load all generated models from the response.

**Parameters:**
- `response`: ModelGenerationResponse from generate_model()

**Returns:**
- Dictionary mapping model names to their corresponding Pydantic model classes

**Raises:**
- `SchemaForgeError`: When model loading fails

### get_model_code

```python
get_model_code(
    response: ModelGenerationResponse
) -> str
```

Get the complete model code including all dependencies and sub-models.

**Parameters:**
- `response`: ModelGenerationResponse from generate_model()

**Returns:**
- Complete Python code string including all model definitions

**Raises:**
- `SchemaForgeError`: When code extraction fails

### get_main_model

```python
get_main_model(
    response: ModelGenerationResponse
) -> Type[BaseModel]
```

Get only the main requested model from the response.

**Parameters:**
- `response`: ModelGenerationResponse from generate_model()

**Returns:**
- The main requested Pydantic model class

**Raises:**
- `SchemaForgeError`: When model loading fails 