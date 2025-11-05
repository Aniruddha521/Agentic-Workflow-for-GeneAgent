from langgraph.graph import END
from gene_agent.states import GeneAgentOverallState

def check_claims(state: GeneAgentOverallState):
    print("---" * 20)
    print(state.proofreader_pass, state.proofreader_count)

    stop_condition = bool(state.proofreader_pass) or (state.proofreader_count > 3)
    print(stop_condition)
    print("---" * 20)

    if stop_condition:
        print("END")
        return END
    
    print("GENERATOR")
    return "generator"
