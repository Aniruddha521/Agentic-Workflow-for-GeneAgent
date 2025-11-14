from gene_agent.states import GeneAgentOverallState
from gene_agent.tools import merge_context
from gene_agent.kg import create_kg_structure, extract_graph_context


def subgraphs_summarization(state: GeneAgentOverallState) -> GeneAgentOverallState:
    graph = create_kg_structure(state)
    results, index, docs = extract_graph_context(graph, state.claims)
    # state.results = [
    #         result['node']+ " " + result['relation'] + " " + result['text']
    #         for _, result in results
    #     ]
    merged_results = merge_context(graph, results)
    state.results = merged_results
    print("---"*20)
    print("summarize")
    print(merged_results)
    print("---"*20)
    state.index = (index, docs)
    state.graph = graph
    return state