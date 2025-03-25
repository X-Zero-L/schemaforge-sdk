"""
SchemaForge SDK Advanced Configuration Examples
This file demonstrates how to use advanced configuration options in the SchemaForge SDK.
"""

from schemaforge import SchemaForge
from pydantic import BaseModel
from typing import List, Optional


def basic_configuration_example():
    """Example showing basic client configuration options"""
    print("\n=== Basic Configuration Example ===")
    
    # Initialize with multiple configuration options
    client = SchemaForge(
        api_key="your_secure_api_key_here",
        api_base="http://localhost:8000",  # Custom API endpoint
        default_model="openai:gpt-4",                 # Default model
        timeout=120.0,                                # Extended timeout (2 minutes)
        max_retries=5,                                # Increased retry attempts
        retry_delay=2.0,                              # Longer delay between retries
        retry_jitter=True,                            # Add randomness to retry timing
        verbose=True                                  # Enable detailed logging
    )
    
    # The rest of your code would use this configured client
    print("Client initialized with custom configuration")


def custom_system_prompt_example():
    """Example showing how to use custom system prompts"""
    print("\n=== Custom System Prompt Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Product(BaseModel):
        name: str
        price: float
        currency: str
        available: bool
    
    # Using a custom system prompt to guide the AI
    product = client.structure(
        content="The new XPS laptop costs $1299 and is currently in stock",
        model_class=Product,
        system_prompt=(
            "You are a specialized data extraction system focused on product information. "
            "Extract product details carefully, using USD as default currency unless specified otherwise. "
            "If availability is not explicitly mentioned, assume the product is available."
        )
    )
    
    print(f"Structured with custom prompt: {product.model_dump()}")


def per_request_model_override():
    """Example showing how to override the model for specific requests"""
    print("\n=== Per-Request Model Override Example ===")
    
    # Initialize with a default model
    client = SchemaForge(
        api_key="your_secure_api_key_here",
        default_model="openai:o3-mini"  # Default to a smaller model
    )
    
    class ComplexData(BaseModel):
        title: str
        description: str
        tags: List[str]
        metadata: Optional[dict]
    
    content = """
    Title: Advanced Machine Learning Techniques
    Description: A comprehensive guide to the latest developments in ML, 
    including transformer architectures and reinforcement learning.
    Tags: machine learning, deep learning, transformers, RL
    Additional info: Published in 2023, 450 pages, second edition
    """
    
    # For complex tasks, override with a more capable model
    complex_data = client.structure(
        content=content,
        model_class=ComplexData,
        model_name="openai:gpt-4"  # Override for this specific request
    )
    
    print(f"Structured with model override: {complex_data.model_dump()}")


def schema_description_example():
    """Example showing how to include schema descriptions"""
    print("\n=== Schema Description Example ===")
    
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    class Person(BaseModel):
        """A person with basic identification and contact information."""
        name: str
        """Full name of the person"""
        age: int
        """Age in years"""
        email: Optional[str] = None
        """Email address if available"""
    
    # Include schema descriptions in the system prompt
    person = client.structure(
        content="Jane Doe is 28 years old, you can reach her at jane.doe@example.com",
        model_class=Person,
        is_need_schema_description=True  # Include model and field descriptions
    )
    
    print(f"Structured with schema descriptions: {person.model_dump()}")


if __name__ == "__main__":
    basic_configuration_example()
    custom_system_prompt_example()
    per_request_model_override()
    schema_description_example() 