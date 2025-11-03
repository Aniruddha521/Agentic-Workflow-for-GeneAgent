from pydantic import BaseModel
from typing import Callable, Any
from typing import Annotated
from .process import ProcessState
from .reducers import (
    not_none_reducer,
    context_reducer,
    process_reducer
)

class GeneAgentSingleGeneState(BaseModel):
    claims: Annotated[str, not_none_reducer]
    process_names: Annotated[ProcessState, process_reducer]
    curated_context: Annotated[Any, context_reducer] = None
    attached_tool: Annotated[Callable, not_none_reducer] = None
    gene: Annotated[str, not_none_reducer] = ""