def pathway_context_reducer(left : list | None, right : list | None) -> set:
    if left is None and right is None:
        return set()
    if left is None:
        return right
    if right is None:
        return left
    return left + right