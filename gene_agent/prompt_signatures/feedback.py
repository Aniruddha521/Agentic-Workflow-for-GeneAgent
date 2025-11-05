import dspy

class Feedback(dspy.Signature):
    """
    Feedback on the generated claims and whether the claims are completly correct or not.
    If claims are not completly correct then `is_correct` field is `False` else `True`.
    Provide proper reason and feedback in the `feedback` field.
    """
    feedback: str = dspy.OutputField(
            desc="""
            Feedback on the generated claims regarding their correctness based on the provided context
            and justification.
            """
        )
    is_correct: bool = dspy.OutputField( 
            desc="""
            A boolean field indicating whether the generated claims are completely correct (`True`)
            or not (`False`) based on the provided context and justification.
            """
        )