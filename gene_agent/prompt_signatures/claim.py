import dspy

class Claim(dspy.Signature):
    """A claim about pathways associated with genes or vice-versa."""
    generated_claim: str = dspy.OutputField(
            desc="""
            The corrected claims regarding the pathways and individual feature of the genes.
            Make sure that the corrected claims are accurate and consistent with the provided context.
            Make sure the length of the corrected claims and query are nearly similar/same and it
            shouldn't contains any reasoning(not even partially).
            """
        )
    justification: str = dspy.OutputField( 
            desc="""
            A detailed justification explaining how the correction were derived from the provided context.
            This should include references to specific pieces of information from the context that support the correction.
            All the reasoning and reference must be included in justification field only
            """
        )