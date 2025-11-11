from gene_agent.states import GeneAgentOverallState
from gene_agent.kg import create_kg_structure, extract_graph_context


def subgraphs_summarization(state: GeneAgentOverallState) -> GeneAgentOverallState:
    graph = create_kg_structure(state)
    results, index, docs = extract_graph_context(graph, state.claims)
    # state.results = [
    #         result['node']+ " " + result['relation'] + " " + result['text']
    #         for _, result in results
    #     ]
    state.results = results
    # print("---"*20)
    # print(results)
    # print("---"*20)
    state.index = (index, docs)
    return state