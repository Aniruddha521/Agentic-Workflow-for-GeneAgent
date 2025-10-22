from gene_agent.states import GeneAgentOverallState
from gene_agent.knowledge_graph import create_kg_structure


def subgraphs_summarization(state: GeneAgentOverallState) -> GeneAgentOverallState:
    graph = create_kg_structure(state)
    return state