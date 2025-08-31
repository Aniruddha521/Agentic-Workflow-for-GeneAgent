from gene_agent.states.process import ProcessState

def process_reducer(left: ProcessState | None, right: ProcessState | None) -> ProcessState:
    if left is None and right is None:
        return ProcessState()
    if left is None:
        return right
    if right is None:
        return left
    return left | right