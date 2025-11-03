import dspy
from .claim import Claim

class ClaimGeneratorSignature(dspy.Signature):
    """
    You are tasked with modifying/correctifying query from a the provided context.
    You don't assume anything beyond the provided context.
    If something not mentioned in the context, you state that it's not available in the context.
    Your output must strictly follow the required JSON schema with only the fields specified below.
    Do not include any explanations, instructions, reasoning steps, or extra fields outside this schema.
    The output must be a valid JSON object that can be parsed by dspy.JSONAdapter.
    """
    retrieved_context: list[str] = dspy.InputField(
            desc="""
                The retrieved context contains relevant information that may assist in verifying and correction
                of claims about the genes, pathways and individual features of the genes provided in the query.
                It's is also helpful in ensuring that the claims are well-informed and based on existing knowledge.
                """
        )
    query: str = dspy.InputField(
            desc="""
                The query containts a claim about one or more genes and pathways.
                The query may turn out to be incomplete or partially incorrect or fully incorrect.
                Your task is to generate accurate claims about their pathways
                and individual features based on the provided genes and context.
                """
        )
    claims: Claim = dspy.OutputField(
            desc="The corrected claims regarding the pathways and individual feature of the genes."
        )
    