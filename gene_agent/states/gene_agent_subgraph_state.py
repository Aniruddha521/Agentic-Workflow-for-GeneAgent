from pydantic import BaseModel

class GeneAgentSubgraphState(BaseModel):
    claims: str
    subgraph_process_names: str
    curated_context: str = ""
    gene: str = ""