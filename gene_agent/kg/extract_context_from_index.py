from .sematic_kg_indexing import SematicKGIndexing

def extract_index_context(index_and_docs, query: list, **kwarg) -> list[tuple]:
    sem = SematicKGIndexing()
    sem.index = index_and_docs[0]
    passages = [f"{d['node']} {d['relation']} {d['text']}" for d in index_and_docs[1]]
    sem.docs.extend(passages)
    if kwarg.get('type') == 'cos':
        results = sem.search([query], top_k=10)
    else:
        results = sem.range_search([query], epsilon=0.5)
    
    return results