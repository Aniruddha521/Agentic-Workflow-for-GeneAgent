from pydantic import BaseModel
from typing import Annotated, Any
from .process import ProcessState
from .reducers import (
    not_none_reducer,
    context_reducer,
    process_reducer,
    pathway_context_reducer
)

class GeneAgentOverallState(BaseModel):
    claims: Annotated[str, not_none_reducer]
    analytical_narrative: Annotated[str, not_none_reducer]
    original_process_names: Annotated[ProcessState, process_reducer]
    curated_context: Annotated[Any, context_reducer] = None
    pathway_context: Annotated[list, pathway_context_reducer] = None
    genes: list[str] = []
    index: Any = None
    results: list[dict] = []
    feedback: str = ""
    proofreader_pass: bool = True
    proofreader_count: int = 0