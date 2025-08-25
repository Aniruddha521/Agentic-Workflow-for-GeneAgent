from langgraph.graph import StateGraph, START, END
from gene_agent.states import GeneAgentSubgraphState
from gene_agent.nodes import (
    fetching_databases, 
    fetch_domain_specific_database,
    verify_and_modify_claims
)
from gene_agent.conditional_edges import (
    parallel_fetching,
    check_claims
)

subgraph_builder = StateGraph(GeneAgentSubgraphState)

subgraph_builder.add_node("fetch_databases", fetching_databases)
subgraph_builder.add_node("fetch_domain_specific_context", fetch_domain_specific_database)
subgraph_builder.add_node("verify_and_modify_claims",verify_and_modify_claims)



subgraph_builder.add_edge(START, "fetch_databases")
subgraph_builder.add_conditional_edges(
    "fetch_databases",
    parallel_fetching,
    ["fetch_domain_specific_context"]
)
subgraph_builder.add_edge("fetch_domain_specific_context", "verify_and_modify_claims")
subgraph_builder.add_conditional_edges(
    "verify_and_modify_claims",
    check_claims,
    ["fetch_domain_specific_context", END]
)

