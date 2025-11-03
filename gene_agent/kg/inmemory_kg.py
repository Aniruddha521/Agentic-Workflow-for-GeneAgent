from collections import defaultdict, deque
from typing import List, Tuple
import os
import re
import numpy as np
import networkx as nx
from pyvis.network import Network
from sentence_transformers import SentenceTransformer
import webbrowser
import os

class InMemoryKG:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.triples = set()
        self.aliases = defaultdict(set)
        self.model = SentenceTransformer("cambridgeltl/SapBERT-from-PubMedBERT-fulltext")

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

    def node_candidates_from_question(self, question: str) -> List[str]:
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
                                             query_terms,
                                             top_n: int = 3) -> List[Tuple[float, str]]:
        """
        Return list of (score, sentence) from node.node_id's 'details' or 'text' using semantic search.
        query_terms can be a list or a string. If model is None, will try to use self.model if present.
        """

        node = self.graph.nodes.get(node_id, {})
        text = node.get("details") or node.get("text") or ""
        if not text:
            return []

        sentences = [s.strip() for s in re.split(r'(?<=[\.\?\!])\s+', text) if s.strip()]
        if not sentences:
            return []

        # use provided model or fallback to self.model if available

        # normalize query_terms
        if isinstance(query_terms, (list, tuple)):
            q_text = " ".join(map(str, query_terms))
        else:
            q_text = str(query_terms)

        # quick substring matching (prefer exact substring hits)
        # q_tokens = [t.lower() for t in re.findall(r"[A-Za-z0-9_\-]+", q_text)]
        # if q_tokens:
        #     hits = []
        #     for s in sentences:
        #         s_low = s.lower()
        #         if any(tok in s_low for tok in q_tokens):
        #             hits.append((1.0, s))
        #     if hits:
        #         return hits[:top_n]

        # if self.model is None:
        #     return [(0.0, s) for s in sentences[:top_n]]

        try:
            emb_q = self.model.encode([q_text], convert_to_numpy=True, show_progress_bar=False)
            emb_sent = self.model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)

            emb_q = np.asarray(emb_q)
            emb_sent = np.asarray(emb_sent)

            if emb_q.ndim == 1:
                emb_q = emb_q.reshape(1, -1)
            if emb_sent.ndim == 1:
                emb_sent = emb_sent.reshape(1, -1)

            # if emb_sent.shape[1] != emb_q.shape[1]:
            #     return [(0.0, s) for s in sentences[:top_n]]

            q_norms = np.linalg.norm(emb_q, axis=1, keepdims=True)
            q_norms[q_norms == 0] = 1.0
            s_norms = np.linalg.norm(emb_sent, axis=1, keepdims=True)
            s_norms[s_norms == 0] = 1.0

            emb_q = emb_q / q_norms
            emb_sent = emb_sent / s_norms

            sims = (emb_sent @ emb_q.T).squeeze()
            sims = np.asarray(sims).reshape(-1)[: len(sentences)]

            scored = sorted([(float(sims[i]), sentences[i]) for i in range(len(sentences))], reverse=True)
            return scored[:top_n]
        except Exception as e:
            return None#[(0.0, s) for s in sentences[:top_n]]

    def is_doc_node_id(self, nid: str) -> bool:
        nd = self.graph.nodes.get(nid, {})
        if not nd:
            return False
        if "details" in nd or "text" in nd:
            return True
        t = str(nd.get("type", "")).lower()
        return t in ("details", "detail description", "document")
    
    def extract_evidence_subgraph(self,
                                  entities: List[str],
                                  query_terms: List[str] = None,
                                  max_hops: int = 2,
                                  include_document_snippets: bool = True,
                                  doc_snippet_top_n: int = 3):
        
        seeds = list(entities)
        q = deque()
        dist = {}
        for s in seeds:
            q.append((s, 0))
            dist[s] = 0
        seen = set(seeds)

        evidence = defaultdict(lambda: defaultdict(set))
        doc_snippets = {}

        while q:
            node, d = q.popleft()
            if d >= max_hops:
                continue

            node_is_doc = self.is_doc_node_id(node)

            # outgoing edges
            for _, tgt, data in self.graph.out_edges(node, data=True):
                relation = data.get("relation", "")

                tgt_is_doc = self.is_doc_node_id(tgt)

                # If either the source (node) or the target (tgt) is a document node,
                # do NOT add that pair to evidence. We still may extract snippets if target is doc.
                if (not node_is_doc) and (not tgt_is_doc):
                    evidence[node][relation].add(tgt)

                if tgt_is_doc and include_document_snippets:
                    snippets = self.extract_relevant_sentences_from_node(tgt, query_terms, top_n=doc_snippet_top_n)
                    if snippets:
                        doc_snippets[tgt] = snippets

                if tgt not in seen:
                    seen.add(tgt)
                    q.append((tgt, d + 1))
                    dist[tgt] = min(dist.get(tgt, 1e9), d + 1)

            for src, _, data in self.graph.in_edges(node, data=True):
                relation = data.get("relation", "")

                src_is_doc = self.is_doc_node_id(src)

                # if (not node_is_doc) and (not src_is_doc):
                #     evidence[node][relation].add(src)

                if src_is_doc and include_document_snippets:
                    query_terms = list(entities) + [relation, node, src]
                    snippets = self.extract_relevant_sentences_from_node(src, query_terms, top_n=doc_snippet_top_n)
                    if snippets:
                        doc_snippets[src] = snippets

                if src not in seen:
                    seen.add(src)
                    q.append((src, d + 1))
                    dist[src] = min(dist.get(src, 1e9), d + 1)

        evidence_out = {}
        for n, relmap in evidence.items():
            if not relmap:
                continue
            evidence_out[n] = {rel: list(neis) for rel, neis in relmap.items() if neis}

        return evidence_out, doc_snippets, dist

    def flatten_kg_dict(self, kg_dict):
        docs = []
        for node, props in kg_dict.items():
            for rel, values in props.items():
                if isinstance(values, list):
                    for v in values:
                        docs.append({
                            "node": node,
                            "relation": rel,
                            "text": v
                        })
                elif isinstance(values, str):
                    docs.append({
                        "node": node,
                        "relation": rel,
                        "text": values
                    })
        return docs

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
