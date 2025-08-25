from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from gene_agent.states import (
    GeneAgentInputState,
    GeneAgentOverallState
)
from gene_agent.nodes import (
    claim_generator,
    subgraphs_summarization
)
from gene_agent.conditional_edges import continue_to_subgraph_block
from gene_agent.subgraph_block import subgraph_builder

memory = MemorySaver()

graph_builder = StateGraph(
    GeneAgentOverallState,
    input=GeneAgentInputState,
    output=GeneAgentOverallState,
)


graph_builder.add_node("generator_node", claim_generator)
graph_builder.add_node("subgraph_block", subgraph_builder.compile())
graph_builder.add_node("summary_node", subgraphs_summarization)

graph_builder.add_edge(START, "generator_node")
graph_builder.add_conditional_edges(
    "generator_node", continue_to_subgraph_block, ["subgraph_block"]
)
graph_builder.add_edge("subgraph_block", "summary_node")
graph_builder.add_edge("summary_node", END)
graph = graph_builder.compile()