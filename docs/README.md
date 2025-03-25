# SchemaForge SDK Documentation

This directory contains detailed documentation for the SchemaForge SDK.

## Contents

- [Installation](installation.md)
- [Getting Started](getting_started.md)
- [Core Concepts](core_concepts.md)
- [API Reference](api_reference.md)
- [Examples](examples/README.md)
  - [Text Structuring](examples/text_structuring.md)
  - [Model Generation](examples/model_generation.md)
  - [Working with Complex Models](examples/complex_models.md)
  - [Async Operations](examples/async_operations.md)
- [Advanced Usage](advanced_usage.md)
- [Error Handling](error_handling.md)
- [FAQ](faq.md)

## Quick Navigation

### Basic Functionality

- [Structuring Text Data](examples/text_structuring.md)
- [Generating Models from Text](examples/model_generation.md)

### Advanced Topics

- [Custom Configurations](advanced_usage.md#custom-configurations)
- [Working with Multiple Models](examples/complex_models.md)
- [Asynchronous Operations](examples/async_operations.md)
- [Error Handling Strategies](error_handling.md)

## Example Usage

Here are some quick examples of using the SchemaForge SDK:

### Text Structuring

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

client = SchemaForge(api_key="your_secure_api_key_here")

class Person(BaseModel):
    name: str
    age: int
    occupation: str
    email: str

person = client.structure(
    content="John is a 30-year-old software engineer with email john@example.com",
    model_class=Person
)
print(person.model_dump())
```

### Model Generation

```python
sample_data = """
This is a smart watch product, model number P12345, priced at $199.99, currently in stock.
The watch features a 6.5-inch display, SnapDragon 8 processor, 128GB storage, and a 48MP camera.
The product is available in Black, Silver, and Gold colors, officially released on January 15, 2024.
"""

response = client.generate_model(
    sample_data=sample_data,
    model_name="Product",
    description="Product information model with specifications"
)

# Get all generated models
models = client.load_generated_model(response)
```

For more detailed information, check out the specific documentation sections. 