from collections import defaultdict, deque
from typing import List, Tuple, Dict
import os
import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
# from sentence_transformers import SentenceTransformer, util
import webbrowser
import os

class InMemoryKG:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.triples = set()
        self.aliases = defaultdict(set)

    def add_node(self, node_id: str, **attrs):
        self.graph.add_node(node_id, **attrs)

    def add_relation(self, subj: str, pred: str, obj: str, **meta):
        """Add an edge and a stored triple."""
        self.triples.add((subj, pred, obj))
        self.graph.add_edge(subj, obj, relation=pred, **(meta or {}))

    def add_alias(self, node: str, alias: str):
        self.aliases[alias.lower()].add(node)

    def export_triples(self) -> List[Tuple[str, str, str]]:
        return list(self.triples)

    def _node_candidates_from_question(self, question: str) -> List[str]:
        q = question
        found = set()

        for token in re.findall(r"[A-Za-z0-9_\-]+", q):
            token_l = token.lower()
            if token_l in self.aliases:
                found.update(self.aliases[token_l])

        for tok in re.findall(r"\b[A-Za-z0-9]{1,25}\b", q):
            if tok in self.graph.nodes:
                found.add(tok)
            if tok.lower() in self.aliases:
                found.update(self.aliases[tok.lower()])

        for n in self.graph.nodes:
            if n.lower() in q.lower():
                found.add(n)

        return list(found)
    
    def extract_relevant_sentences_from_node(self,
                                             node_id: str,
                                             query_terms: List[str],
                                             model=None,
                                             top_n: int = 3) -> List[Tuple[float, str]]:
        
        node = self.graph.nodes.get(node_id, {})
        text = node.get("details") or ""
        if not text:
            return []

        sentences = [s.strip() for s in re.split(r'(?<=[\.\?\!])\s+', text) if s.strip()]

        if model is not None:
            try:
                q_text = " ".join(query_terms)
                emb_q = model.encode([q_text], convert_to_numpy=True, show_progress_bar=False)
                emb_sent = model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)
                emb_q = emb_q / np.linalg.norm(emb_q, axis=1, keepdims=True)
                emb_sent = emb_sent / np.linalg.norm(emb_sent, axis=1, keepdims=True)
                sims = (emb_sent @ emb_q.T).squeeze()
                scored = sorted([(float(sims[i]), sentences[i]) for i in range(len(sentences))], reverse=True)
                return scored[:top_n]
            except Exception:
                return [(0.0, s) for s in sentences[:top_n]]

        return [(0.0, s) for s in sentences[:top_n]]
    
    def extract_evidence_subgraph(self,
                                  entities: List[str],
                                  max_hops: int = 2,
                                  include_document_snippets: bool = True,
                                  model=None,
                                  doc_snippet_top_n: int = 3):
        
        seeds = list(entities)
        q = deque()
        dist = {}
        for s in seeds:
            q.append((s, 0))
            dist[s] = 0
        seen = set(seeds)
        evidence = set()
        doc_snippets = {}  # node_id -> list[(score, sentence)]

        while q:
            node, d = q.popleft()
            if d >= max_hops:
                continue
            for _, tgt, data in self.graph.out_edges(node, data=True):
                relation = data.get("relation", "")
                evidence.add((node, relation, tgt))
                # if target looks like a document and we want snippets, extract
                tgt_node = self.graph.nodes.get(tgt, {})
                is_doc = ("text" in tgt_node) or (tgt_node.get("type", "").lower() in ("details", "document"))
                if is_doc and include_document_snippets:
                    # query_terms = entities + relation + node labels (you might tune this)
                    query_terms = list(entities) + [relation] + [node, tgt]
                    snippets = self.extract_relevant_sentences_from_node(tgt, query_terms, model=model, top_n=doc_snippet_top_n)
                    if snippets:
                        doc_snippets[tgt] = snippets
                if tgt not in seen:
                    seen.add(tgt)
                    q.append((tgt, d + 1))
                    dist[tgt] = min(dist.get(tgt, 1e9), d + 1)
            # incoming
            for src, _, data in self.graph.in_edges(node, data=True):
                relation = data.get("relation", "")
                evidence.add((src, relation, node))
                src_node = self.graph.nodes.get(src, {})
                is_doc = ("text" in src_node) or (src_node.get("type", "").lower() in ("details", "document"))
                if is_doc and include_document_snippets:
                    query_terms = list(entities) + [relation] + [node, src]
                    snippets = self.extract_relevant_sentences_from_node(src, query_terms, model=model, top_n=doc_snippet_top_n)
                    if snippets:
                        doc_snippets[src] = snippets
                if src not in seen:
                    seen.add(src)
                    q.append((src, d + 1))
                    dist[src] = min(dist.get(src, 1e9), d + 1)

        return evidence, doc_snippets, dist

    def find_common_neighbors_of_type(self, nodes: List[str], node_type_label: str = "Pathway") -> List[str]:
        common = None
        for n in nodes:
            nbrs = set(self.graph.successors(n)) | set(self.graph.predecessors(n))
            if common is None:
                common = nbrs
            else:
                common = common.intersection(nbrs)
        if not common:
            return []
        res = []
        for c in common:
            ntype = self.graph.nodes[c].get("type")
            if node_type_label is None or ntype == node_type_label:
                res.append(c)
        return res

    def shortest_paths_between(self, node_a: str, node_b: str, cutoff: int = 4):
        try:
            paths = list(nx.all_simple_paths(self.graph.to_undirected(), source=node_a, target=node_b, cutoff=cutoff))
        except nx.NetworkXNoPath:
            paths = []
        return paths
    
    def plot_interactive(self, output_file="graph.html", open_browser=True):
        net = Network(notebook=False, directed=True)

        for subj, obj, data in self.graph.edges(data=True):
            relation = data.get('relation', '')
            net.add_node(subj, label=subj, color="#89CFF0")
            net.add_node(obj, label=obj, color="#FFD580")
            net.add_edge(subj, obj, label=relation)

        net.repulsion(node_distance=200, spring_length=200, damping=0.9)

        net.write_html(output_file)
        print(f"Interactive graph saved to: {output_file}")

        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))


def demo():
    kg = InMemoryKG()

    # Add example nodes with types (fictional toy data)
    kg.add_node("ERBB2", type="Gene")
    kg.add_node("ERBB4", type="Gene")
    kg.add_node("MAPK_pathway", type="Pathway")
    kg.add_node("PI3K_AKT_pathway", type="Pathway")
    kg.add_node("Breast_Carcinoma", type="Disease")

    # Add relations (triples)
    kg.add_relation("ERBB2", "participates_in", "MAPK_pathway")
    kg.add_relation("ERBB2", "participates_in", "PI3K_AKT_pathway")
    kg.add_relation("ERBB4", "participates_in", "MAPK_pathway")
    kg.add_relation("ERBB4", "participates_in", "PI3K_AKT_pathway")
    kg.add_relation("ERBB2", "associated_with", "Breast_Carcinoma")
    kg.add_relation("ERBB4", "associated_with", "Breast_Carcinoma")

    # aliasing
    kg.add_alias("ERBB2", "ERBB2")
    kg.add_alias("ERBB4", "ERBB4")
    kg.add_alias("Breast_Carcinoma", "breast cancer")

    # Build semantic index
    idx = SemanticKGIndex(kg)
    idx.build_index()

    # Example question (from your user scenario)
    question = (
        "Disease caused by ERBB2 and ERBB4 genes and in which pathways we can find the both of the genes "
        "and will it increases the disease causing factor?"
    )

    # 1) Entity linking + BFS evidence extraction
    entities = kg._node_candidates_from_question(question)
    print("Entities found:", entities)
    evidence, dist = kg.extract_evidence_subgraph(entities, max_hops=2)
    ranked_by_graph = []
    for (s, p, o) in evidence:
        # simple score: shorter distance preferred
        d = min(dist.get(s, 10), dist.get(o, 10))
        score = 10.0 / (1 + d)
        ranked_by_graph.append((score, (s, p, o)))
    ranked_by_graph.sort(reverse=True, key=lambda x: x[0])

    # 2) Semantic retrieval over triple sentences
    sem_results = idx.query(question, top_k=8)
    print("\nTop semantic matches (score, triple_text):")
    for score, txt, tri in sem_results:
        print(f"{score:.4f}\t{txt}")

    # Compose final candidate facts: take top semantic + top graph-scored
    sem_triples = [r[2] for r in sem_results]
    graph_triples = [t for _, t in ranked_by_graph[:8]]
    # merge preserving order and uniqueness
    seen = set()
    merged = []
    for t in sem_triples + graph_triples:
        if t not in seen:
            merged.append(t); seen.add(t)

    facts = triples_to_sentences(merged[:10])
    common_pathways = kg.find_common_neighbors_of_type(entities, "Pathway")

    print("\nFacts to pass to LLM:\n")
    for f in facts:
        print(f)

    # Build prompt
    prompt = build_prompt_from_facts(question, facts, common_pathways)

    # Optionally call OpenAI
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        print("\nCalling OpenAI... (this requires OPENAI_API_KEY set)")
        answer = ask_openai_with_prompt(prompt)
        print("\nLLM answer:\n", answer)
    else:
        print("\nOpenAI not configured. Here is the prompt you can send to an LLM:\n")
        print(prompt)


if __name__ == "__main__":
    demo()
