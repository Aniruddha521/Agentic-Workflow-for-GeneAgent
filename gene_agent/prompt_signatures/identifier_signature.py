import dspy
from .entities import Entities

class IdentifierSignature(dspy.Signature):
    """
    You are tasked with generating claims from a given list of genes.
    Your output must strictly follow the required JSON schema with only the fields specified below.
    Do not include any explanations, instructions, reasoning steps, or extra fields outside this schema.
    The output must be a valid JSON object that can be parsed by dspy.JSONAdapter.
    """
    query: str = dspy.InputField(
            desc="""
                The query contains one or more genes for which claims about their pathways 
                and individual features need to be generated.
                """
        )
    entities: Entities = dspy.OutputField(
            desc="The generated claims regarding the pathways and individual feature of the genes."
        )