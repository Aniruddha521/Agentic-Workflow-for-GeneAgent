import dspy
from .feedback import Feedback

class ProofReaderSignature(dspy.Signature):
    """
    You are tasked to verify and provide feedback on the generated claims based on the context.
    If in the claim there is any incorrect or missing information based on the context, you need to point it out 
    and provide the feedback.
    Also make sure that the claims are well-aligned with the context.
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
    justification: str = dspy.InputField(
            desc="""
                The justification contains the reasoning behind the generated claims.
                Your task is to verify the claim and give feedback based on the justification 
                and provided context.
                """
        )
    response: Feedback = dspy.OutputField(
            desc="""
            The feedback on the generated claims regarding their correctness based on the provided context
            and justification.
            """
        )
    