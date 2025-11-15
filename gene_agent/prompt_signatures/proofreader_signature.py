import dspy
from .feedback import Feedback

class ProofReaderSignature(dspy.Signature):
    """
    You are an assistant that verifies the correctness and completeness of a generated claim
    using ONLY the retrieved_context and justification.

    STRICT RULES:

    1. You must NOT use any prior knowledge. Only information explicitly present in the 
       retrieved_context may be used to evaluate the query.

    2. The query must be checked for:
       - factual correctness
       - completeness
       - consistency with justification
       - missing or unsupported entities
       - incorrect relationships

    3. COMPLETENESS RULE (Important):
       If the query lists multiple entities belonging to the same relationship 
       (e.g., "gene1, gene2, gene3 are involved in pathway X"), you MUST verify whether 
       ALL entities in the retrieved_context that share this relationship are included.
       
       - If any such entity is missing from the query, the query is INCOMPLETE.
       - An incomplete query MUST be marked incorrect.
       - Feedback must clearly list the missing entities.

       Partial lists are NOT considered correct unless the query explicitly states 
       that it is only listing “some” entities.

    4. If the query includes an entity or relationship not supported by the context, 
       you must mark it as incorrect and explain why.

    5. If the justification does not align with the query or contradicts the context,
       you must flag the inconsistency.

    6. The final output must strictly follow the Feedback JSON schema with ONLY the fields 
       defined in the schema. Do not include reasoning outside those fields.

    7. The output must be valid JSON parsable by dspy.JSONAdapter.
    """

    retrieved_context: list[str] = dspy.InputField(
        desc="""
            List of factual statements used as the ONLY source of truth.
            These statements may describe individual gene–pathway relationships.
            You must aggregate them when checking completeness of multi-entity claims.
        """
    )

    query: str = dspy.InputField(
        desc="""
            The generated claim to verify. It may contain correct information, incorrect 
            information, missing entities, or incomplete grouped claims.
        """
    )

    justification: str = dspy.InputField(
        desc="""
            The reasoning used to form the query. You must ensure that the justification 
            aligns with the context and supports (or contradicts) the query.
        """
    )

    response: Feedback = dspy.OutputField(
        desc="""
            Structured feedback describing whether the query is correct and complete, 
            and identifying any missing, incorrect, or unsupported facts.
        """
    )
