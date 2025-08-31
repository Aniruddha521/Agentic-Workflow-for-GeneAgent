from gene_agent.states import GeneAgentSingleGeneState

def single_gene_data_fetching(state: GeneAgentSingleGeneState) -> GeneAgentSingleGeneState:
    tool = state.attached_tool
    context = tool(state.gene)

    # print("---"*20)
    # print(context)
    # print("---"*20)

    state.curated_context = context

    return state