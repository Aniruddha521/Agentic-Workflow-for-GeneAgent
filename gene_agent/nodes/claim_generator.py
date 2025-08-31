import os
import dspy
from dotenv import load_dotenv
from gene_agent.states import GeneAgentOverallState, ProcessState
from gene_agent.prompt_signatures import ClaimsGeneratorSignature
from gene_agent.tools import get_pubmed_articles

dspy.settings.configure(cache=None)
def claim_generator(state: GeneAgentOverallState) -> GeneAgentOverallState:
    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    generator = dspy.ChainOfThought(ClaimsGeneratorSignature)
    llm = dspy.LM(
            model="huggingface/openai/gpt-oss-120b", 
            api_key=api_key
    )
    with dspy.context(lm=llm):
        response = generator(
            query=state.claims,
        )
    process_name = response.claim.original_process_name
    process_details = get_pubmed_articles(process_name)
    process = ProcessState(
        process_names = process_name,
        detail = process_details
    )
    state.original_process_names = process
    state.original_analytical_narrative = response.claim.original_analytical_narratives
    state.genes = response.claim.genes
    
    return state


# [huggingface/deepseek-ai/DeepSeek-V3.1:fireworks-ai] //can be used dor calling deepseek model from huggingface