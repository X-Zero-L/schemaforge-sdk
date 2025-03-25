# Getting Started with SchemaForge SDK

This guide will help you get started with the SchemaForge SDK for data structuring and model generation.

## Installation

Install the SchemaForge SDK using pip:

```bash
pip install schemaforge
```

## Initial Setup

To use the SchemaForge SDK, you'll need an API key. You can initialize the client in two ways:

```python
from schemaforge import SchemaForge

# Option 1: Pass API key directly
client = SchemaForge(api_key="your_secure_api_key_here")

# Option 2: Set environment variable and initialize
# export SCHEMAFORGE_API_KEY=your_secure_api_key_here
client = SchemaForge()
```

## Basic Usage

### Structure Text Data

The core functionality of SchemaForge is converting unstructured text into structured Pydantic models:

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

client = SchemaForge(api_key="your_secure_api_key_here")

# Define your model
class Person(BaseModel):
    name: str
    age: int
    occupation: str
    email: str

# Structure text into your model
person = client.structure(
    content="John is a 30-year-old software engineer with email john@example.com",
    model_class=Person
)

# Access structured data
print(person.model_dump())
# {'name': 'John', 'age': 30, 'occupation': 'software engineer', 'email': 'john@example.com'}
```

### Generate Models from Text

Another powerful feature is generating Pydantic models from text descriptions:

```python
# Natural language description
sample_data = """
This is a smart watch product, model number P12345, priced at $199.99, currently in stock.
The watch features a 6.5-inch display, SnapDragon 8 processor, 128GB storage, and a 48MP camera.
The product is available in Black, Silver, and Gold colors, officially released on January 15, 2024.
"""

# Generate model
response = client.generate_model(
    sample_data=sample_data,
    model_name="Product",
    description="Product information model with specifications"
)

if response.success:
    # Load all generated models
    models = client.load_generated_model(response)
    
    # Access the main model
    product_model = models["Product"]
    
    # Get the model code for saving or further use
    model_code = client.get_model_code(response)
    print(model_code)
```

## Next Steps

- Explore [asynchronous operations](async_operations.md) for improved performance
- Learn about [custom configuration options](custom_configuration.md) for advanced usage
- See the [API reference](api_reference.md) for detailed method documentation 