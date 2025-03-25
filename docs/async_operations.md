# Asynchronous Operations

SchemaForge SDK supports asynchronous operations for improved performance in I/O-bound applications. This document describes how to use these async capabilities.

## Asynchronous Methods

SchemaForge provides async versions of its core methods:

| Synchronous Method | Asynchronous Equivalent |
|-------------------|-------------------------|
| `structure()`     | `astructure()`          |
| `generate_model()`| `agenerate_model()`     |

## Basic Usage

### Asynchronous Text Structuring

```python
import asyncio
from pydantic import BaseModel
from schemaforge import SchemaForge

async def main():
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Person(BaseModel):
        name: str
        age: int
        occupation: str
    
    # Async call
    person = await client.astructure(
        content="Jane is a 25-year-old data scientist", 
        model_class=Person
    )
    
    print(person.model_dump())
    # {'name': 'Jane', 'age': 25, 'occupation': 'data scientist'}

asyncio.run(main())
```

### Asynchronous Model Generation

```python
import asyncio
from schemaforge import SchemaForge

async def main():
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    sample_data = """
    This is a laptop product, model X1 Carbon, priced at $1299.99.
    It features a 14-inch display, Intel i7 processor, 16GB RAM, and 512GB SSD.
    """
    
    # Async model generation
    response = await client.agenerate_model(
        sample_data=sample_data,
        model_name="Laptop",
        description="Laptop product information model"
    )
    
    if response.success:
        models = client.load_generated_model(response)
        main_model = models["Laptop"]
        print(main_model.model_json_schema())

asyncio.run(main())
```

## Parallel Processing

Async operations are particularly useful for parallel processing:

```python
import asyncio
from pydantic import BaseModel
from schemaforge import SchemaForge

class Person(BaseModel):
    name: str
    age: int
    occupation: str

async def process_texts(texts):
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    # Process multiple texts in parallel
    tasks = [
        client.astructure(content=text, model_class=Person)
        for text in texts
    ]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    return results

async def main():
    texts = [
        "Jane is a 25-year-old data scientist",
        "Bob is a 32-year-old teacher",
        "Alice is a 40-year-old engineer"
    ]
    
    people = await process_texts(texts)
    for person in people:
        print(person.model_dump())

asyncio.run(main())
```

## Performance Considerations

- Async operations are most beneficial for I/O-bound workloads
- For CPU-bound tasks, consider using multiprocessing instead
- Batch processing with async operations can significantly improve throughput 