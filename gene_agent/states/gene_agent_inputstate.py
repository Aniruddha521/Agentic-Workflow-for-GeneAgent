from pydantic import BaseModel


class GeneAgentInputState(BaseModel):
    claims: str
