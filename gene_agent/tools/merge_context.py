from collections import Counter, OrderedDict
import re
from .custom_structures import ContextNodeRelation
from gene_agent.kg.inmemory_kg import InMemoryKG

def structure_context(kg: InMemoryKG, context: list[str]) -> dict:
    nodes = set()
    relations = set()
    passages = {}
    for q in context:
        remove_node = kg.node_candidates_from_question(q)
        nodes.update(remove_node)
        pattern = '|'.join(re.escape(x) for x in remove_node)
        relation = re.sub(pattern, '', q).strip()
        extract_relation = lambda relation: " ".join(
            t for t in re.split(r'[^A-Za-z0-9_]+', relation) if t.strip()
        )
        relation = extract_relation(relation)
        if len(relation) > 25:
            relation = relation.split(" ")[0]
        if relation not in relations:
            relations.add(relation)
            passages[relation] = []
        # sorted_nodes = sorted(remove_node, key=lambda x: q.find(x))
        passages[relation].append(
            ContextNodeRelation.from_string(q, relation)
        )
    return passages

def ordered_unique(kg, seq):
    out = set()
    for item in seq:
        nodes = kg.node_candidates_from_question(item)
        out.update(nodes)
    return list(out)

def merge_relations(kg, data):
    merged = []
    
    for relation, pairs in data.items():

        if isinstance(pairs, list) and len(pairs) == 1 and isinstance(pairs[0], str):
            merged.append([f"{pairs[0]} {relation}"])
            print("Descriptive relation:", relation)
            continue
        
        # only handle list-of-pairs
        if not isinstance(pairs, list) or not pairs:
            print("Not a list of pairs for relation:", relation)
            continue
        
        # filter valid pairs
        # for p in pairs:
        #     if isinstance(p, GraphEntities):
        #         print(p)
        valid_pairs = [(p.prefix, p.suffix) for p in pairs if isinstance(p, ContextNodeRelation)]
        if not valid_pairs:
            # print("No valid pairs for relation:", relation)
            # print(valid_pairs)
            continue
        
        left_counts = Counter(a for a,b in valid_pairs)
        right_counts = Counter(b for a,b in valid_pairs)
        
        max_left = max(left_counts.values()) if left_counts else 0
        max_right = max(right_counts.values()) if right_counts else 0
        
        group_by_right = max_right >= max_left
        if group_by_right:
            groups = OrderedDict()
            for subj, obj in valid_pairs:
                groups.setdefault(obj.strip(), []).append(subj)
            for obj, subjects in groups.items():
                subjects = ordered_unique(kg, subjects)
                if len(subjects) == 1:
                    stmt = f"{subjects[0]} {relation} {obj}"
                else:
                    stmt = f"{', '.join(subjects)} {relation} {obj}"
                merged.append([stmt])
        else:
            groups = OrderedDict()
            for subj, obj in valid_pairs:
                groups.setdefault(subj.strip(), []).append(obj)
            for subj, objects in groups.items():
                objects = ordered_unique(kg, objects)
                if len(objects) == 1:
                    stmt = f"{subj} {relation} {objects[0]}"
                else:
                    stmt = f"{subj} {relation} {', '.join(objects)}"
                merged.append([stmt])

    return merged

def merge_context(kg: InMemoryKG, context: list[str]) -> list:
    structured = structure_context(kg, context)
    merged = merge_relations(kg, structured)
    return_context = []
    for item in merged:
        return_context.append(item[0])
    return return_context
