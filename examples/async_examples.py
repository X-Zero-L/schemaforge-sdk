"""
SchemaForge SDK Asynchronous Operations Examples
This file demonstrates how to use the asynchronous capabilities of the SchemaForge SDK.
"""

import asyncio
import time
from typing import List, Dict, Any
from pydantic import BaseModel
from schemaforge import SchemaForge


async def basic_async_structure():
    """Basic example of asynchronous text structuring"""
    print("\n=== Basic Async Structure Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Person(BaseModel):
        name: str
        age: int
        occupation: str
    
    # Async structuring
    start = time.time()
    person = await client.astructure(
        content="Jane is a 25-year-old data scientist",
        model_class=Person
    )
    end = time.time()
    
    print(f"Result: {person.model_dump()}")
    print(f"Time taken: {end - start:.2f} seconds")


async def basic_async_generate_model():
    """Basic example of asynchronous model generation"""
    print("\n=== Basic Async Model Generation Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    sample_data = """
    This is a laptop product, model X1 Carbon, priced at $1299.99.
    It features a 14-inch display, Intel i7 processor, 16GB RAM, and 512GB SSD.
    """
    
    # Async model generation
    start = time.time()
    response = await client.agenerate_model(
        sample_data=sample_data,
        model_name="Laptop",
        description="Laptop product information model"
    )
    end = time.time()
    
    if response.success:
        models = client.load_generated_model(response)
        print(f"Generated model: {models['Laptop'].model_json_schema()['title']}")
        print(f"Time taken: {end - start:.2f} seconds")
    else:
        print(f"Model generation failed: {response.error}")


async def parallel_processing():
    """Example of processing multiple requests in parallel"""
    print("\n=== Parallel Processing Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Person(BaseModel):
        name: str
        age: int
        occupation: str
    
    # Data to process
    texts = [
        "Jane is a 25-year-old data scientist",
        "Bob is a 32-year-old teacher",
        "Alice is a 40-year-old software engineer",
        "Mike is a 28-year-old graphic designer",
        "Sara is a 35-year-old doctor"
    ]
    
    # Process sequentially first for comparison
    print("Sequential processing:")
    sequential_start = time.time()
    sequential_results = []
    for text in texts:
        person = await client.astructure(content=text, model_class=Person)
        sequential_results.append(person)
    sequential_end = time.time()
    print(f"Time taken (sequential): {sequential_end - sequential_start:.2f} seconds")
    
    # Process in parallel
    print("\nParallel processing:")
    parallel_start = time.time()
    tasks = [client.astructure(content=text, model_class=Person) for text in texts]
    parallel_results = await asyncio.gather(*tasks)
    parallel_end = time.time()
    print(f"Time taken (parallel): {parallel_end - parallel_start:.2f} seconds")
    
    # Show speed improvement
    speedup = (sequential_end - sequential_start) / (parallel_end - parallel_start)
    print(f"Speedup factor: {speedup:.2f}x")
    
    # Show results
    print("\nResults:")
    for i, person in enumerate(parallel_results):
        print(f"Person {i+1}: {person.model_dump()}")


async def concurrent_different_operations():
    """Example of running different operations concurrently"""
    print("\n=== Concurrent Different Operations Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Person(BaseModel):
        name: str
        age: int
        occupation: str
    
    class Product(BaseModel):
        name: str
        price: float
        currency: str
        in_stock: bool
    
    # Define sample data for model generation
    sample_data = """
    Smart TVs with 4K resolution, ranging from 42" to 65", priced between $399 and $1299.
    They feature HDMI ports, USB ports, and built-in streaming apps.
    Most popular models include Samsung Q60, LG C1, and Sony X80J.
    """
    
    # Run different operations concurrently
    start = time.time()
    structure_task = client.astructure(
        content="Jane is a 25-year-old data scientist",
        model_class=Person
    )
    
    product_task = client.astructure(
        content="Samsung Q60 Smart TV costs $799 and is currently available",
        model_class=Product
    )
    
    model_gen_task = client.agenerate_model(
        sample_data=sample_data,
        model_name="TV",
        description="Smart TV product information model"
    )
    
    # Wait for all tasks to complete
    person, product, model_response = await asyncio.gather(
        structure_task, product_task, model_gen_task
    )
    end = time.time()
    
    # Display results
    print(f"Person: {person.model_dump()}")
    print(f"Product: {product.model_dump()}")
    
    if model_response.success:
        models = client.load_generated_model(model_response)
        print(f"Generated model: {models['TV'].model_json_schema()['title']}")
    
    print(f"Time taken (concurrent): {end - start:.2f} seconds")


async def main():
    """Run all examples"""
    await basic_async_structure()
    await basic_async_generate_model()
    await parallel_processing()
    await concurrent_different_operations()


if __name__ == "__main__":
    asyncio.run(main()) 