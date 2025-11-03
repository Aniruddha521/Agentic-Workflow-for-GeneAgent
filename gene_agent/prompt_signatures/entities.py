import dspy

class Entities(dspy.Signature):
    """Identify the entities (genes, pathways, etc.) from the given query."""
    original_process_name: str = dspy.OutputField(
            desc="The name of pathways associated with the claim."
        )
    genes: list[str] = dspy.OutputField(
            desc="The list of genes for which claims about their pathways and individual features are generated."
        )