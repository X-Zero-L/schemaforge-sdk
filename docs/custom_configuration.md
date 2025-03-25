# Custom Configuration

SchemaForge SDK offers various configuration options to customize its behavior. This document explains the available configuration options and how to use them.

## Client Configuration

When initializing the SchemaForge client, you can customize its behavior with various parameters:

```python
from schemaforge import SchemaForge

client = SchemaForge(
    api_key="your_secure_api_key_here",
    api_base="http://localhost:8000",
    default_model="openai:gpt-4",
    timeout=120.0,
    max_retries=5,
    retry_delay=2.0,
    retry_jitter=True,
    verbose=True
)
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `api_key` | API key for authentication | `SCHEMAFORGE_API_KEY` env var |
| `api_base` | Base URL for API requests | `SCHEMAFORGE_API_BASE` env var |
| `default_model` | Default AI model to use | Provider's default |
| `timeout` | Request timeout in seconds | 60.0 |
| `max_retries` | Maximum number of retry attempts | 3 |
| `retry_delay` | Initial delay for retries in seconds | 1.0 |
| `retry_jitter` | Whether to add random jitter to retry delays | True |
| `verbose` | Whether to enable verbose logging | False |

## Method-Level Configuration

You can override the default configuration at the method level:

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

client = SchemaForge(api_key="your_secure_api_key_here")

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Override model at method level
person = client.structure(
    content="John is a 30-year-old software engineer",
    model_class=Person,
    model_name="openai:gpt-4"  # Override default model
)
```

## Custom System Prompts

You can provide custom system prompts to guide the AI model:

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

client = SchemaForge(api_key="your_secure_api_key_here")

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Add custom system prompt
person = client.structure(
    content="John is a 30-year-old software engineer",
    model_class=Person,
    system_prompt="Extract the person information accurately and infer any missing data carefully."
)
```

## Environment Variables

SchemaForge SDK supports configuration via environment variables:

```bash
# Set API key
export SCHEMAFORGE_API_KEY="your_secure_api_key_here"

# Set custom API base URL
export SCHEMAFORGE_API_BASE="http://localhost:8000"
```

These environment variables will be used by default if no explicit parameters are provided during client initialization. 