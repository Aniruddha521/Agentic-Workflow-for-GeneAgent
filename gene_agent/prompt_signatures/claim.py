import dspy

class Claim(dspy.Signature):

    original_analytical_narratives: str = dspy.OutputField(
            desc="The generated claims regarding the pathways and individual feature of the genes."
        )
    original_process_name: str = dspy.OutputField(
            desc="The name of pathways associated with the claim."
        )
    genes: list[str] = dspy.OutputField(
            desc="The list of genes for which claims about their pathways and individual features are generated."
        )