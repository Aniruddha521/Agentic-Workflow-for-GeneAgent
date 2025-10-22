import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import webbrowser
import os


class InMemoryKG:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.triples = set()

    def add_relation(self, subj, pred, obj, meta=None):
        """Add a relation (triple) to the in-memory knowledge graph."""
        self.triples.add((subj, pred, obj))
        self.graph.add_edge(subj, obj, relation=pred, **(meta or {}))

    def query(self, entity):
        """Return all outgoing relations for a given entity."""
        return [(entity, data['relation'], tgt) 
                for _, tgt, data in self.graph.out_edges(entity, data=True)]

    def export_triples(self):
        """Export all stored triples as a list."""
        return list(self.triples)

    def plot_interactive(self, output_file="graph.html", open_browser=True):
        """
        Create an interactive visualization of the knowledge graph using PyVis.
        Works both in scripts and Jupyter notebooks.
        """
        net = Network(notebook=False, directed=True)

        for subj, obj, data in self.graph.edges(data=True):
            relation = data.get('relation', '')
            net.add_node(subj, label=subj, color="#89CFF0")
            net.add_node(obj, label=obj, color="#FFD580")
            net.add_edge(subj, obj, label=relation)

        net.repulsion(node_distance=200, spring_length=200, damping=0.9)

        net.write_html(output_file)
        print(f"✅ Interactive graph saved to: {output_file}")

        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))
