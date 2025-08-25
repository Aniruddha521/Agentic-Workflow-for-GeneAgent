from pydantic import BaseModel

class GeneAgentOverallState(BaseModel):
    claims: str
    origonial_analytical_narrative: str
    original_process_names: str
    genes: list[str] = []