from .sematic_kg_indexing import SematicKGIndexing

def extract_index_context(index_and_docs, query: list) -> list[tuple]:
    sem = SematicKGIndexing()
    sem.index = index_and_docs[0]
    sem.docs = index_and_docs[1]
    results = sem.range_search([query], epsilon=0.7)
    
    return results