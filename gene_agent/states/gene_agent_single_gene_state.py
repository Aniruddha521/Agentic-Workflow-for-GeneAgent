from pydantic import BaseModel
from typing import Callable

class GeneAgentSingleGeneState(BaseModel):
    claims: str
    process_names: str
    curated_context: str = ""
    attached_tool: Callable = None
    gene: str = ""