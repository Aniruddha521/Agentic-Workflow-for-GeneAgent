import dspy

class Claim(dspy.Signature):
    """
    A corrected claim about genes and there behaviour.
    """

    generated_claim: str = dspy.OutputField(
        desc="""
            The corrected claim rewritten strictly using the retrieved_context 
            and (when appropriate) the feedback.

            Requirements:
            - The corrected claim MUST NOT include any reasoning, justification, or explanation.
            - Length and structure must be similar to the original query.
            - Only facts explicitly stated in the retrieved_context may appear.
            - If the query mentions an entity not present in the context, 
              the claim must state that the information is not available in the context.
        """
    )

    justification: str = dspy.OutputField(
        desc="""
            A concise explanation describing HOW the corrected claim was derived.
            Requirements:
            - Justification must reference the specific context statements used.
            - All reasoning MUST be placed here and ONLY here.
            - Justification should not introduce new facts beyond what appears 
              in the retrieved_context.
            - If feedback was ignored due to irrelevance, this must be stated here.
            - If information was unavailable in context, this must also be noted here.
        """
    )
