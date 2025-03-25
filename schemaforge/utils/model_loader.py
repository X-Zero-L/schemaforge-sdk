"""
Utilities for loading Pydantic models from generated code.
"""

import sys
import re
import logging
import tempfile
import os
from typing import Type, Any, Dict, List, Optional, Match, Pattern, Union
from pydantic import BaseModel
from importlib.machinery import SourceFileLoader


logger = logging.getLogger("schemaforge")


def load_model_from_code(model_code: str, model_name: Optional[str] = None) -> Type[BaseModel]:
    """
    Load a Pydantic model from generated code string.
    
    This function supports two methods of loading the model:
    1. A safer method using a temporary module (default, recommended)
    2. Direct execution using exec() (fallback, less safe)
    
    Args:
        model_code: Python code string containing a Pydantic model definition
        model_name: Optional name of the model to extract (required if multiple models defined)
        
    Returns:
        The Pydantic model class
        
    Raises:
        ValueError: If no Pydantic model is found or multiple models are found 
                   without specifying which one to use
    """
    try:
        return _load_model_via_module(model_code, model_name)
    except Exception as e:
        logger.warning(f"Failed to load model via module: {e}. Falling back to exec method.")
        return _load_model_via_exec(model_code, model_name)


def _load_model_via_module(model_code: str, model_name: Optional[str] = None) -> Type[BaseModel]:
    """
    Load a Pydantic model by creating a temporary module file.
    
    This is a safer approach than using exec() as it properly handles imports
    and maintains Python's module system integrity.
    
    Args:
        model_code: Python code string containing a Pydantic model definition
        model_name: Optional name of the model to extract
        
    Returns:
        The Pydantic model class
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp_file:
        tmp_filepath = tmp_file.name
        tmp_file.write(model_code.encode('utf-8'))
    
    try:
        # Extract module name from path (without .py extension)
        module_name = os.path.basename(tmp_filepath)[:-3]
        
        # Load the module
        loader = SourceFileLoader(module_name, tmp_filepath)
        module = loader.load_module()
        
        # Find model classes in the module
        model_classes = {
            name: obj for name, obj in module.__dict__.items()
            if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel
        }
        
        if not model_classes:
            raise ValueError("No Pydantic model found in the generated code")
        
        # Return the specified model or handle multiple models
        if model_name and model_name in model_classes:
            return model_classes[model_name]
        elif len(model_classes) == 1:
            return list(model_classes.values())[0]
        else:
            names = list(model_classes.keys())
            if model_name:
                raise ValueError(f"Model '{model_name}' not found. Available models: {names}")
            else:
                raise ValueError(f"Multiple models found ({names}). Please specify which one to use.")
        
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filepath):
            os.unlink(tmp_filepath)


def _load_model_via_exec(model_code: str, model_name: Optional[str] = None) -> Type[BaseModel]:
    """
    Load a Pydantic model using exec().
    
    This is a fallback method when the module-based approach fails.
    Note: This method uses exec() which should only be used with trusted inputs.
    
    Args:
        model_code: Python code string containing a Pydantic model definition
        model_name: Optional name of the model to extract
        
    Returns:
        The Pydantic model class
    """
    # Create a namespace for the model
    namespace: Dict[str, Any] = {}
    
    # Add common imports to the namespace
    import_code = """
from typing import Optional, List, Dict, Any, Union, Literal
from datetime import datetime, date, time
from pydantic import BaseModel, Field, validator, root_validator
"""
    
    # Execute the imports and model code in this namespace
    exec(import_code, namespace)
    exec(model_code, namespace)
    
    # Find all model classes in the namespace
    model_classes = {
        name: obj for name, obj in namespace.items()
        if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel
    }
    
    if not model_classes:
        raise ValueError("No Pydantic model found in the generated code")
    
    # Return the specified model or handle multiple models
    if model_name and model_name in model_classes:
        return model_classes[model_name]
    elif len(model_classes) == 1:
        return list(model_classes.values())[0]
    else:
        names = list(model_classes.keys())
        if model_name:
            raise ValueError(f"Model '{model_name}' not found. Available models: {names}")
        else:
            raise ValueError(f"Multiple models found ({names}). Please specify which one to use.") 