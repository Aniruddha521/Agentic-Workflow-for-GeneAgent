import dspy
from .claim import Claim

class ClaimGeneratorSignature(dspy.Signature):
    """
    Your task is to correct or regenerate the claims in the query using ONLY the retrieved_context
    and (when relevant) the feedback.

    STRICT RULES:
    1. You must not use any prior knowledge outside the retrieved_context.
    2. The corrected claims must remain similar in length and structure to the original query.
    3. Use the feedback to fix mistakes in the query ONLY if the feedback is relevant. 
       - If the feedback is empty or irrelevant, you must ignore it and state this clearly 
         inside the Claim schema’s justification field.
    4. If the query references any entity (gene, pathway, process, feature, etc.) that does not appear
       in the retrieved_context, you MUST explicitly state that the information is not available in
       the context.
    5. You must not assume or infer missing facts. If a relationship is not explicitly described in
       the retrieved_context, treat it as unsupported.
    6. The output MUST strictly follow the Claim JSON schema and contain ONLY the fields defined in it.
       No explanations, no reasoning steps, and no extra fields.
    7. The final output MUST be a valid JSON object parsable by dspy.JSONAdapter.
    """

    retrieved_context: list[str] = dspy.InputField(
        desc="""
            A list of factual statements describing gene–pathway relationships or gene features.
            These are the ONLY facts allowed for constructing the corrected claims.
            If a fact does not appear here, treat it as unavailable or unsupported.
        """
    )

    feedback: str = dspy.InputField(
        desc="""
            Feedback describing errors, missing facts, or contradictions in the query.
            Use it to correct the query ONLY when it directly applies to it.
            If irrelevant or empty, you must ignore it (with justification inside the Claim output).
        """
    )

    query: str = dspy.InputField(
        desc="""
            The original claim involving one or more genes, pathways, or gene features.
            The query may be incomplete, partially incorrect, or fully incorrect.
            Your task is to produce a corrected version grounded strictly in the retrieved_context.
        """
    )

    claims: Claim = dspy.OutputField(
        desc="""
            The corrected claims that align with the retrieved_context and (when relevant) the feedback.
            Must follow the Claim JSON schema exactly with no extra fields.
        """
    )
