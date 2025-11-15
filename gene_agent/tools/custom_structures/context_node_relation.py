from dataclasses import dataclass

@dataclass
class ContextNodeRelation:
    prefix: str = ""
    suffix: str = ""

    @classmethod
    def from_string(cls, q, relation):
        prefix, suffix = (q.split(relation) + ["", ""])[:2]
        return cls(prefix=prefix, suffix=suffix)
    
    @classmethod
    def item(cls):
        return cls.prefix, cls.suffix
