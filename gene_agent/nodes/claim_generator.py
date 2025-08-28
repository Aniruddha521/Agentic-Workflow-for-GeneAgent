import os
import dspy
from dotenv import load_dotenv
from gene_agent.states import GeneAgentOverallState
from gene_agent.prompt_signatures import ClaimsGeneratorSignature

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
    state.original_process_names = response.claim.original_process_name
    state.original_analytical_narrative = response.claim.original_analytical_narratives
    state.genes = response.claim.genes
    
    return state


# huggingface/deepseek-ai/DeepSeek-V3.1:fireworks-ai