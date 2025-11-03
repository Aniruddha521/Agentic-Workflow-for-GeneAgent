from .inmemory_kg import InMemoryKG
from .sematic_kg_indexing import SematicKGIndexing

def extract_graph_context(graph: InMemoryKG, query: list) -> list[tuple]:
    entities = graph.node_candidates_from_question(query)
    evidence, node_docs, _ = graph.extract_evidence_subgraph(entities, query, max_hops=4)
    print(node_docs)
    node_docs = [
        {
            "node": node,
            "relation": "details",
            "text": "\n".join(text for _, text in snippets)
        }
        for node, snippets in node_docs.items()
    ]
    docs = graph.flatten_kg_dict(evidence)
    docs.extend(node_docs)
    sem = SematicKGIndexing()
    index = sem.index_docs(docs)
    results = sem.search([query], top_k=100)
    
    return results, index