"""
SchemaForge SDK Usage Examples
This file demonstrates how to use the SchemaForge SDK for data structuring and model generation.
"""

import asyncio
from typing import Dict, Type
from pydantic import BaseModel
from schemaforge import SchemaForge


def main():
    # Initialize SDK
    client = SchemaForge(
        api_key="your_secure_api_key_here",
        api_base="http://localhost:8000",
        default_model="openai:o3-mini",
    )

    # Example 1: Structure text using predefined model
    print("\n=== Example 1: Text Structuring ===")

    class Person(BaseModel):
        name: str
        age: int
        occupation: str
        email: str

    # Synchronous call
    person = client.structure(
        content="John is a 30-year-old software engineer with email john@example.com",
        model_class=Person,
    )
    print(f"Structured result: {person.model_dump()}")

    # Example 2: Generate model from sample data
    print("\n=== Example 2: Model Generation ===")

    # Use natural language description
    sample_data = """
    This is a smart watch product, model number P12345, priced at $199.99, currently in stock.
    The watch features a 6.5-inch display, SnapDragon 8 processor, 128GB storage, and a 48MP camera.
    The product is available in Black, Silver, and Gold colors, officially released on January 15, 2024.
    """

    # Generate model
    response = client.generate_model(
        sample_data=sample_data,
        model_name="Product",
        description="Product information model with basic info, specifications, and color options",
    )

    if response.success:
        print("✅ Model generation successful!")
        print(f"Model name: {response.model_name}")

        # Get all generated models (including sub-models)
        models: Dict[str, Type[BaseModel]] = client.load_generated_model(response)
        print("\nGenerated models:")
        for name, model in models.items():
            print(f"\n{name}:")
            print(model.model_json_schema())

        # Get only the main model
        main_model = client.get_main_model(response)
        print("\nMain model:")
        print(main_model.model_json_schema())

        # Get the complete code
        complete_code = client.get_model_code(response)
        print("\nComplete code:")
        print(complete_code)
    else:
        print(f"❌ Model generation failed: {response.error}")


async def async_examples():
    print("\n=== Example 3: Asynchronous Calls ===")

    client = SchemaForge(api_key="your_secure_api_key_here")

    # Asynchronous text structuring
    class Person(BaseModel):
        name: str
        age: int
        occupation: str

    person = await client.astructure(
        content="Jane is a 25-year-old data scientist", model_class=Person
    )
    print(f"Asynchronous structuring result: {person.model_dump()}")

    # Asynchronous model generation
    sample_data = """
    This is a high-performance laptop, priced at $999.99, currently in stock.
    The laptop features an Intel i7 processor, 16GB RAM, and 512GB SSD storage.
    The body is made of aluminum alloy, weighs about 1.5kg, and has a battery life of up to 8 hours.
    """

    response = await client.agenerate_model(
        sample_data=sample_data,
        model_name="Laptop",
        description="Laptop information model with specifications",
    )

    if response.success:
        print("✅ Asynchronous model generation successful!")
        models = client.load_generated_model(response)
        print("\nGenerated models:")
        for name, model in models.items():
            print(f"\n{name}:")
            print(model.model_json_schema())
    else:
        print(f"❌ Asynchronous model generation failed: {response.error}")


if __name__ == "__main__":
    # Run synchronous examples
    main()

    # Run async examples
    asyncio.run(async_examples())
