
def not_none_reducer(left : str | None, right : str | None) -> str:
    if left is None and right is None:
        return ""
    if left is None:
        return right
    if right is None:
        return left
    return right