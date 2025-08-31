from gene_agent.states import GeneAgentMultiGenesState

def gene_set_data_fetching(state: GeneAgentMultiGenesState) -> GeneAgentMultiGenesState:
    tool = state.attached_tool
    print(state.genes)
    print(type(state.genes))
    context = tool(state.genes)
    state.pathway_context = context

    return state