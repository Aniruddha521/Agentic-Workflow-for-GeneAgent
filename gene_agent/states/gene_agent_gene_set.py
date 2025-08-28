from pydantic import BaseModel
from typing import Callable

class GeneAgentMultiGenesState(BaseModel):
    claims: str
    process_names: str
    curated_context: str = ""
    attached_tool: Callable = None
    genes: list[str] = []