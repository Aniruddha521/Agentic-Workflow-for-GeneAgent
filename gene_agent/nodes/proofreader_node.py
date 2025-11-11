import os
import dspy
from dotenv import load_dotenv
from gene_agent.states import GeneAgentOverallState
from gene_agent.prompt_signatures import ProofReaderSignature
from gene_agent.kg import extract_index_context
from gene_agent.tools import find_difference

dspy.settings.configure(cache=None)
def verify_claims(state: GeneAgentOverallState) -> GeneAgentOverallState:
    load_dotenv()
    query = find_difference(state.prev_claims, state.claims)
    
    results = extract_index_context(state.index, query, type='cos')
    state.results.extend(results)
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    proofreader = dspy.ChainOfThought(ProofReaderSignature)
    llm = dspy.LM(
            model="huggingface/deepseek-ai/DeepSeek-R1:novita", 
            api_key=api_key
    )
    with dspy.context(lm=llm):
        response = proofreader(
            retrieved_context = state.results,
            # justification = state.analytical_narrative,
            query=state.claims
        )
    state.feedback = response.response.feedback
    state.proofreader_pass = response.response.is_correct
    state.proofreader_count += 1
    print("---"*20)
    print("proofreader")
    print(query)
    print(results)
    print(state.proofreader_pass)
    print("---"*20)
    return state


# [huggingface/deepseek-ai/DeepSeek-V3.2-Exp:novita] //can be used for calling deepseek V3.2 model from huggingface
# [huggingface/deepseek-ai/DeepSeek-R1:novita] //can be used for calling deepseek R1 model from huggingface
# [huggingface/openai/gpt-oss-120b] //can be used for calling gpt-oss model from huggingface
# [huggingface/Qwen/Qwen3-Next-80B-A3B-Instruct:novita] //can be used for calling Qwen3-Next-80B-A3B-Instruct model from huggingface