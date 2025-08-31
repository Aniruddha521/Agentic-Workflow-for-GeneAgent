from typing import Any

def context_reducer(left: Any | None, right: Any | None) -> Any:
    if left is None and right is None:
        return None
    if left is None:
        return right
    if right is None:
        return left
    
    whole_context = left + right
    sorted_context = merge_sort(whole_context, 0, len(whole_context)-1)
    final_context = []
    i = 0
    while i < len(sorted_context):
        j = i
        disease = []
        domain = []
        complexes = []
        while j < len(sorted_context) and sorted_context[j]['gene_name'] == sorted_context[i]['gene_name']:
            disease.extend(sorted_context[j].get('diseases', []))
            domain.extend(sorted_context[j].get('domains', []))
            complexes.extend(sorted_context[j].get('complexes', []))
            j += 1
        unique_context = {
                'gene_name' : sorted_context[j-1]['gene_name'],
                'diseases': disease,
                'domains': domain,
                'complexes': complexes
            }
        final_context.append(unique_context)
        i = j
    return final_context

def merge_sort(context, left, right):

    if left >= right:
        return

    mid = (left + right)//2
    merge_sort(context, left, mid)
    merge_sort(context, mid+1, right)
    merge(context, left, mid, right)

    return context

def merge(context, left, mid, right):
    i = left
    j = mid + 1
    k = 0
    temp = [None] * (right - left + 1)

    while i <= mid and j <= right:
        if context[i]["gene_name"] <= context[j]["gene_name"]:
            temp[k] = context[i]
            i += 1
        else:
            temp[k] = context[j]
            j += 1
        k += 1

    while i <= mid:
        temp[k] = context[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = context[j]
        j += 1
        k += 1

    for p in range(len(temp)):
        context[left + p] = temp[p]

    return context