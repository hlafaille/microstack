"""
Schemas for the Abstract Syntax Tree.
---
The Microstack AST serves as a way to go from a list of `Service` schema(s) to executable and repeatable
Python code.
"""
from pydantic import BaseModel


class AstNetwork(BaseModel):
    """Defining a unique Network defined under a Service"""

