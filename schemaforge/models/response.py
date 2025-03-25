from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class StructureResponse(BaseModel):
    """Response schema for structured data."""

    success: bool = Field(..., description="Whether processing was successful")
    data: Dict[str, Any] = Field(..., description="Structured data")
    error: Optional[str] = Field(None, description="Error message")
    model_used: str = Field(..., description="The model used for processing")


class ModelFieldDefinition(BaseModel):
    """Definition of a single field for a model."""

    name: str = Field(..., description="Field name")
    field_type: str = Field(
        ..., description="Field type (string, integer, number, boolean, array, etc.)"
    )
    description: str = Field(..., description="Description of the field")
    required: bool = Field(True, description="Whether the field is required")
    default: Optional[Any] = Field(None, description="Default value for the field")


class ModelGenerationResponse(BaseModel):
    """Response schema for model generation."""

    success: bool = Field(..., description="Whether model generation was successful")
    model_name: str = Field(..., description="Name of the generated model")
    model_code: str = Field(
        ..., description="Generated model code in Python using Pydantic"
    )
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON Schema representation of the generated model, suitable for use in any programming language",
    )
    fields: List[ModelFieldDefinition] = Field(
        ..., description="List of fields in the generated model"
    )
    model_used: str = Field(..., description="The model used for generation")
    error: Optional[str] = Field(None, description="Error message if generation failed")
