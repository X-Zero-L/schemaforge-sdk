# SchemaForge SDK Documentation

This directory contains detailed documentation for the SchemaForge SDK.

## Contents

- [Getting Started](getting_started.md)
- [API Reference](api_reference.md)

## Quick Navigation

### Basic Functionality

- [Structuring Text Data](examples/text_structuring.md)
- [Generating Models from Text](examples/model_generation.md)

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