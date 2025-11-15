from langgraph.graph import END
from gene_agent.states import GeneAgentOverallState

def check_claims(state: GeneAgentOverallState):
    stop_condition = bool(state.proofreader_pass) or (state.proofreader_count > 3)

    if stop_condition:
        print("END")
        return END
    
    print("GENERATOR")
    return "generator"
