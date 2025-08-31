from pydantic import BaseModel
from typing import Annotated
from .reducers import not_none_reducer


class GeneAgentInputState(BaseModel):
    claims: Annotated[str, not_none_reducer]
