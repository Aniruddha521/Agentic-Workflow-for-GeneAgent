import dspy
from .feedback import Feedback

class ProofReaderSignature(dspy.Signature):
    """
    You are an assistant that verifies the correctness of a generated claim using ONLY:
    - the retrieved_context
    - the justification
    STRICT RULES:
    1. You must NOT use prior knowledge. Ignore anything not present in the retrieved_context.
    2. If the query contains any incorrect facts, contradictions, missing information, or missing / extra entities 
       (genes, processes, diseases, domains, complexes, etc.) relative to the retrieved_context:
       - you MUST identify them clearly
       - you MUST provide corrective feedback in the output
    3. All feedback must be grounded entirely in the retrieved_context.
    4. Your output MUST strictly follow the JSON schema of the Feedback object.
       - Do NOT add extra fields.
       - Do NOT include explanations, reasoning steps, or instructions outside the schema.
    5. The final output must be valid JSON that can be parsed by dspy.JSONAdapter.

    Your goal: ensure that the query is fully aligned with the retrieved_context and justification, 
    pointing out any factual errors, inconsistencies, omissions, or unsupported claims.
    """
    retrieved_context: list[str] = dspy.InputField(
            desc="""
                A list of context passages that contain all the information allowed for verification.
                You MUST rely exclusively on this context while checking the query.
                If the context does not explicitly support a part of the query, you must flag it.
                """
        )
    query: str = dspy.InputField(
            desc="""
                The generated claim that must be verified.
                The claim may contain errors, missing entities (e.g., genes, processes,
                diseases, domains, complexes), or incomplete information.
                Your task is to evaluate this claim strictly against the retrieved_context.
                """
        )
    justification: str = dspy.InputField(
            desc="""
                The reasoning used to produce the query.
                You must evaluate whether the justification is aligned with the retrieved_context
                and whether it supports or contradicts the query.
                """
        )
    response: Feedback = dspy.OutputField(
            desc="""
            The final structured feedback about the query.
            Feedback must identify:
              - factual correctness or incorrectness
              - missing or unsupported entities
              - inconsistencies between query, context, and justification
            """
        )
    