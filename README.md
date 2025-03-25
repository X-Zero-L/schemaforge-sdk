# SchemaForge Python SDK

<div align="center">
  <p>
    <strong>AI-Powered Data Structuring Tool</strong>
  </p>
  <p>
    <a href="https://github.com/X-Zero-L/schemaforge-sdk"><strong>GitHub</strong></a> ·
    <a href="https://github.com/X-Zero-L/schemaforge-sdk/docs"><strong>Documentation</strong></a> ·
    <a href="https://github.com/X-Zero-L/schemaforge-sdk"><strong>Website</strong></a>
  </p>
</div>

English | [中文](./README_CN.md)

## About

This is the official Python SDK for [SchemaForge AI](https://github.com/X-Zero-L/schemaforge-ai), a unified service for AI structured data processing using Pydantic models to define output formats, supporting multiple AI large language models.

## Installation

```bash
pip install schemaforge
```

## Quick Start

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

# Initialize client
client = SchemaForge(api_key="your_secure_api_key_here")

# Define a Pydantic model
class Person(BaseModel):
    name: str
    age: int
    occupation: str
    email: str

# Structure text using the model
person = client.structure(
    content="John is a 30-year-old software engineer with email john@example.com",
    model_class=Person
)
print(person.model_dump())
# {'name': 'John', 'age': 30, 'occupation': 'software engineer', 'email': 'john@example.com'}
```

## Features

- **Structure unstructured text** into Pydantic models
- **Generate Pydantic models** from natural language descriptions
- **Handle complex model dependencies** automatically
- **Async support** for all operations

## Documentation

See the [complete documentation](https://github.com/X-Zero-L/schemaforge-sdk/tree/master/docs) for detailed examples and API reference. 