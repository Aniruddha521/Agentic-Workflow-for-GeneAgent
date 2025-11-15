import dspy

class Feedback(dspy.Signature):
    """
    Structured feedback evaluating the correctness of the query.

    Rules:
    - The evaluation must be based ONLY on the retrieved_context and justification.
    - If ANY part of the query is unsupported, incorrect, contradictory, or missing
      relative to the retrieved_context, then `is_correct` MUST be False.
    - The `feedback` field must clearly describe what is correct, what is incorrect,
      and which entities or relationships are missing or unsupported.
    - Do NOT add extra fields. Output MUST follow this schema exactly.
    """
    feedback: str = dspy.OutputField(
            desc="""
            A concise but complete explanation identifying:
            - Correct parts of the query (if any)
            - Incorrect or contradictory statements
            - Missing or unsupported entities, relationships, or facts
            - Any mismatch between query, context, and justification
            The feedback must rely ONLY on the retrieved_context and justification.
            """
        )
    is_correct: bool = dspy.OutputField( 
            desc="""
            True ONLY if the entire query is fully supported by the retrieved_context.
            False if:
                - Any entity is missing from the context
                - Any part of the claim contradicts the context
                - The justification does not support the query
                - Any relationship is incomplete or partially supported
            """
        )