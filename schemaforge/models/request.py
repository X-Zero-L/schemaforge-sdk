from typing import Optional, Any, List
from pydantic import BaseModel, Field


class StructuredRequest(BaseModel):
    """Request schema for structuring data."""

    content: str = Field(..., description="Raw text content to be structured")
    schema_description: str = Field(
        ..., description="Expected structured data description"
    )
    system_prompt: Optional[str] = Field(None, description="System prompt (optional)")
    model_name: Optional[str] = Field(
        None,
        description="Model name to use (e.g., 'openai:gpt-4o', 'anthropic:claude-3-opus-latest')",
    )
    is_need_schema_description: bool = Field(
        False,
        description="Whether schema description should be included in system prompt. Default is False as advanced models usually don't need it",
    )
    struct_model_name: Optional[str] = Field(
        "DynamicModel", description="Model name to use for structuring"
    )


class ModelFieldDefinition(BaseModel):
    """Definition of a single field for a model."""

    name: str = Field(..., description="Field name")
    field_type: str = Field(
        ..., description="Field type (string, integer, number, boolean, array, etc.)"
    )
    description: str = Field(..., description="Description of the field")
    required: bool = Field(True, description="Whether the field is required")
    default: Optional[Any] = Field(None, description="Default value for the field")


class ModelGenerationRequest(BaseModel):
    """Request schema for model generation."""

    sample_data: str = Field(
        ..., description="Sample data in text format to analyze for model creation"
    )
    model_name: str = Field(..., description="Name to use for the generated model")
    description: str = Field(
        ..., description="Description of what the model represents"
    )
    requirements: Optional[str] = Field(
        None, description="Specific requirements or expectations for the model"
    )
    expected_fields: Optional[List[ModelFieldDefinition]] = Field(
        None, description="Optional list of expected fields"
    )
    llm_model_name: Optional[str] = Field(
        None,
        description="Model name to use for generation (e.g., 'openai:gpt-4o', 'anthropic:claude-3-opus-latest')",
    )
