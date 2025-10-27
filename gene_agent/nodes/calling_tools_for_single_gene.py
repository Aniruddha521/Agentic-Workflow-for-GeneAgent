from gene_agent.states import GeneAgentSingleGeneState

def single_gene_data_fetching(state: GeneAgentSingleGeneState) -> GeneAgentSingleGeneState:
    tool = state.attached_tool
    context = tool(state.gene)
    state.curated_context = context

    return state