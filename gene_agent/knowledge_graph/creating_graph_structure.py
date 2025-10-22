import networkx as nx
from .inmemory_kg import InMemoryKG
from gene_agent.states import GeneAgentOverallState

graph = InMemoryKG()

def create_kg_structure(state: GeneAgentOverallState) -> InMemoryKG:
    for context in state.curated_context:
        gene = context.get("gene_name")
        for disease in context.get("diseases", []):
            graph.add_relation(gene, "can_cause", disease["disease_caused"])
        for domain in context.get("domains", []):
            graph.add_relation(gene, "has_domain", domain["domain_name"])
        for complex in context.get("complexes", []):
            graph.add_relation(gene, "part_of_complex", complex["complex_ac"])
            graph.add_relation(complex["complex_ac"], "complex_name", complex["complex_name"])

    graph.add_relation(
        state.original_process_names.process_names,
        "details", 
        state.original_process_names.detail
    )
    for pathway in state.pathway_context:
        for gene in pathway.get("overlapping genes").split(","):
            graph.add_relation(gene, "involved_in", pathway.get("term"))
            graph.add_relation(pathway.get("term"), "confirmed_by_database", pathway.get("database"))

    graph.plot_interactive(output_file="knowledge_graph.html", open_browser=True)
    
    return graph
