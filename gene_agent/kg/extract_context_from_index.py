from .sematic_kg_indexing import SematicKGIndexing

def extract_index_context(index, query: list) -> list[tuple]:
    sem = SematicKGIndexing()
    sem.index = index
    results = sem.search([query])
    
    return results