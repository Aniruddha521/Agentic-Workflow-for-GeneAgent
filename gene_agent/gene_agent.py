from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from gene_agent.states import (
    GeneAgentInputState,
    GeneAgentOverallState
)
from gene_agent.nodes import (
    claim_generator,
    subgraphs_summarization,
    gene_set_data_fetching,
    single_gene_data_fetching,
    verify_and_modify_claims
)
from gene_agent.conditional_edges import (
    tool_calling_condition, 
    check_claims
)

memory = MemorySaver()

graph_builder = StateGraph(
    GeneAgentOverallState,
    input=GeneAgentInputState,
    output=GeneAgentOverallState,
)


graph_builder.add_node("generator_node", claim_generator)
graph_builder.add_node("single_gene_data_fetching", single_gene_data_fetching)
graph_builder.add_node("gene_set_data_fetching", gene_set_data_fetching)
graph_builder.add_node("summarize_tools_results", subgraphs_summarization)
graph_builder.add_node("verify_and_modify_claims",verify_and_modify_claims)

graph_builder.add_edge(START, "generator_node")
graph_builder.add_edge("generator_node", END)
# graph_builder.add_conditional_edges(
#     "generator_node", 
#     tool_calling_condition, 
#     [
#         "single_gene_data_fetching",
#         "gene_set_data_fetching"
#     ]
# )
# # graph_builder.add_edge("single_gene_subgraph_block", "summary_node")
# graph_builder.add_edge("single_gene_data_fetching", "summarize_tools_results")
# graph_builder.add_edge("gene_set_data_fetching", "summarize_tools_results")
# graph_builder.add_edge("summarize_tools_results", "verify_and_modify_claims")
# graph_builder.add_conditional_edges(
#     "verify_and_modify_claims",
#     check_claims,
#     ["summarize_tools_results", END]
# )
graph = graph_builder.compile()