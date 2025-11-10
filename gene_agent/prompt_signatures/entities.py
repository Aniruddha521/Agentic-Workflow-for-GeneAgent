import dspy

class Entities(dspy.Signature):
    """Identify the entities (genes, pathways, etc.) from the given query."""
    original_process_name: str = dspy.OutputField(
            desc="The name of pathways associated with the claim."
        )
    genes: list[str] = dspy.OutputField(
            desc="The list of genes for which claims about their pathways and individual features are generated."
        )
    intents: list[str] = dspy.OutputField(
            desc="""
            The list of intents for single gene data fetching, e.g., pathway, disease, domain, complex.
            
            **Pathway**  – A sequence of interconnected biochemical reactions or signaling steps through which genes and proteins carry out a specific biological function.
            **Disease**  – A pathological condition arising from genetic, molecular, or cellular abnormalities that disrupt normal biological processes.
            **Domain**   – A distinct structural or functional region within a protein that determines how it interacts, binds, or performs specific biological tasks.
            **Complex**  – A multi-protein assembly in which several molecules work together to execute a coordinated biological function.
            """
        )