import networkx as nx
from .inmemory_kg import InMemoryKG
from gene_agent.states import GeneAgentOverallState

graph = InMemoryKG()

def create_kg_structure(state: GeneAgentOverallState) -> InMemoryKG:
    for context in state.curated_context:
        gene = context.get("gene_name")
        graph.add_node(gene, type="gene")
        for disease in context.get("diseases", []):
            graph.add_node(disease["disease_caused"], type="disease")
            graph.add_relation(
                gene,
                "causes", 
                disease["disease_caused"], 
                evidences=disease.get("num_of_evidence", 0)
            )
        for domain in context.get("domains", []):
            graph.add_node(domain["domain_name"], type="domain")
            graph.add_relation(
                gene, 
                "has_domain", 
                domain["domain_name"],
                evidences=domain.get("num_of_evidence", 0)
            )
        for complex in context.get("complexes", []):
            graph.add_node(complex["complex_ac"], type="complex")
            graph.add_alias(complex["complex_ac"], complex["complex_name"])
            graph.add_relation(
                gene, 
                "part_of_complex", 
                complex["complex_ac"], 
                evidences=complex.get("num_of_evidence", 0)
            )
    graph.add_node(
        state.original_process_names.process_names, 
        type="process",
        details = state.original_process_names.detail
    )
    for alias in state.original_process_names.process_names.split(' '):
        graph.add_alias(
            state.original_process_names.process_names, 
            alias
        )
    # graph.add_node(
    #     state.original_process_names.detail, 
    #     type="detail description"
    # )
    # graph.add_relation(
    #     state.original_process_names.process_names,
    #     "details", 
    #     state.original_process_names.detail
    # )
    for pathway in state.pathway_context:
        for gene in pathway.get("overlapping genes").split(","):
            graph.add_node(gene, type="gene")
            graph.add_node(pathway.get("term"), type="pathway")
            graph.add_node(pathway.get("database"), type="database")
            graph.add_relation(gene, "involved_in", pathway.get("term"))
            graph.add_relation(
                pathway.get("term"), 
                "confirmed_by_database", 
                pathway.get("database")
            )
    entities = graph._node_candidates_from_question(state.claims)
    evidence, dist = graph.extract_evidence_subgraph(entities, max_hops=4)

    print("---"*20)
    print(entities)
    print(evidence)
    print("---"*20)
    # graph.plot_interactive(output_file="knowledge_graph.html", open_browser=True)
    
    return graph
