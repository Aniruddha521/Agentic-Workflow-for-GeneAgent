import os
import dspy
from dotenv import load_dotenv
from gene_agent.states import GeneAgentOverallState
from gene_agent.prompt_signatures import ClaimGeneratorSignature

dspy.settings.configure(cache=None)
def narrative_generator(state: GeneAgentOverallState) -> GeneAgentOverallState:
    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    generator = dspy.ChainOfThought(ClaimGeneratorSignature)
    llm = dspy.LM(
            model="huggingface/openai/gpt-oss-120b", 
            api_key=api_key
    )
    with dspy.context(lm=llm):
        response = generator(
            retrieved_context = state.results,
            query=state.claims
        )
    state.claims = response.claims.generated_claim
    state.analytical_narrative = response.claims.justification
    
    return state


# [huggingface/deepseek-ai/DeepSeek-V3.1:fireworks-ai] //can be used dor calling deepseek model from huggingface